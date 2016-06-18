import logging

from django.conf import settings
from django.core.urlresolvers import reverse

from oscar.core.loading import get_class, get_model
from oscar.core.exceptions import (
    AppNotFoundError, ClassNotFoundError, ModuleNotFoundError)

Dispatcher = get_class('customer.utils', 'Dispatcher')
CommunicationEventType = get_model('customer', 'CommunicationEventType')
Partner = get_model('partner', 'Partner')
Person = get_model('oscar_ficta', 'Person')
Invoice = get_model('invoice', 'Invoice')

# Standard logger for checkout events
logger = logging.getLogger('oscar.checkout')


class SessionData(object):
    """
    Responsible for marshalling all the site-wide session data

    Proudly grabbed from original oscar.apps.checkout.utils CheckoutSessionData
    """
    # TODO: it would be better to split original class into base and ancestors for checkout etc,
    #       but it requires correct PR for django-oscar

    SESSION_KEY = 'site_data'

    def __init__(self, request):
        self.request = request
        if self.SESSION_KEY not in self.request.session:
            self.request.session[self.SESSION_KEY] = {}

    def _check_namespace(self, namespace):
        """
        Ensure a namespace within the session dict is initialised
        """
        if namespace not in self.request.session[self.SESSION_KEY]:
            self.request.session[self.SESSION_KEY][namespace] = {}

    def _get(self, namespace, key, default=None):
        """
        Return a value from within a namespace
        """
        self._check_namespace(namespace)
        if key in self.request.session[self.SESSION_KEY][namespace]:
            return self.request.session[self.SESSION_KEY][namespace][key]
        return default

    def _set(self, namespace, key, value):
        """
        Set a namespaced value
        """
        self._check_namespace(namespace)
        self.request.session[self.SESSION_KEY][namespace][key] = value
        self.request.session.modified = True

    def _unset(self, namespace, key):
        """
        Remove a namespaced value
        """
        self._check_namespace(namespace)
        if key in self.request.session[self.SESSION_KEY][namespace]:
            del self.request.session[self.SESSION_KEY][namespace][key]
            self.request.session.modified = True

    def _flush_namespace(self, namespace):
        """
        Flush a namespace
        """
        self.request.session[self.SESSION_KEY][namespace] = {}
        self.request.session.modified = True

    def flush(self):
        """
        Flush all session data
        """
        self.request.session[self.SESSION_KEY] = {}


class FictaSessionData(SessionData):

    def pay_as_person(self, person_id):
        self._set('payment', 'person', person_id)

    def get_person_id(self):
        return self._get('payment', 'person')

    def save_found_person_id(self, person_id):
        self._set('payment', 'person_found', person_id)

    def get_found_person_id(self):
        return self._get('payment', 'person_found')

    def save_invoice_number(self, number):
        self._set('payment', 'invoice', number)


class CheckoutSessionMixin(object):
    """some helpers for managing juristic persons during checkout
    """

    def check_person_id(self, id=-1):
        if id != -1:
            try:
                person = Person.browsable.get(pk=id)
            except Person.DoesNotExist:
                pass
            else:
                id = getattr(person, 'id', -1)
        return id

    def get_session(self):
        if hasattr(self, 'user_session'):
            return self.user_session
        else:
            try:
                return get_class('user.session', 'UserSessionData')(self.request)
            except (ImportError, AppNotFoundError, ClassNotFoundError, ModuleNotFoundError):
                return FictaSessionData(self.request)

    def pay_as_person(self, person_id):
        id = self.check_person_id(person_id)

        # trying to use site-wide session instead of checkout one
        # which will be flushed after order placement
        self.get_session().pay_as_person(id)

    def get_person_id(self):
        return self.get_session().get_person_id()

    def save_found_person_id(self, person_id):
        id = self.check_person_id(person_id)
        self.get_session().save_found_person_id(person_id)

    def get_found_person_id(self):
        return self.get_session().get_found_person_id()

    def already_registered(self, person, user):
        # TODO: move it to Person model
        return user in person.users.all()

    def link_user(self, request, person=None):
        if person is None:
            id = self.check_person_id(self.get_found_person_id())
            if id != -1:
                person = Person.browsable.get(pk=id)
            else:
                # cant link user as selected person is user (id=-1)
                return id
        if not self.already_registered(person, request.user):
            person.users.add(request.user)
            person.save()
        return person 
    
    def set_invoice_order(self, order):
        # assigns an order to an invoice 
        # and save invoice in the session 

        # it's possible to get more than one invoice for the order given
        # as of previous failures as of back-button clicked, for example,
        # so we use last one created
        invoices = list(Invoice.objects.filter(order_number__exact=order.number, 
                                               status__exact=Invoice.DRAFT,
                                               order__exact=None).order_by('-date_created'))
        
        if len(invoices) > 0:
            invoice = invoices[0]
            logger.info("Order #%s assigning to invoice #%s", order.number, invoice.number)
            partner = self.get_default_partner(order)
            if len(partner.juristic_persons.values()) > 0:
                invoice.partner_person = partner.juristic_persons.get()
            else:
                # TODO: raise ImproperlyConfigured
                logger.warning("Order #%s: cant find partner's juristic person for invoice", order.number)
                pass
            invoice.order = order
            invoice.status = invoice.NEW
            invoice.save()
            self.get_session().save_invoice_number(invoice.number)

            ctx = {
                'shop_name': settings.OSCAR_SHOP_NAME,
                'user': order.user,
                'invoice': invoice,
                'order': order,
                'print_url': reverse('invoice:print', kwargs={'number': invoice.number})
            }
            communication_type_code = 'INVOICE_SENT'
            try:
                event_type = CommunicationEventType.objects.get(code=communication_type_code)
            except CommunicationEventType.DoesNotExist:
                # No event-type in database, attempt to find templates for this
                # type and render them immediately to get the messages.  Since we
                # have not CommunicationEventType to link to, we can't create a
                # CommunicationEvent instance.
                messages = CommunicationEventType.objects.get_and_render(communication_type_code, ctx)
                event_type = None
            else:
                messages = event_type.get_messages(ctx)

            if messages and messages['body']:
                logger.info("Invoice #%s - sending %s messages", invoice.number, communication_type_code)
                dispatcher = Dispatcher(logger)
                dispatcher.dispatch_order_messages(order, messages,
                                                   event_type)
            else:
                logger.warning("Invoice #%s - no %s communication event type",
                               invoice.number, communication_type_code)

        else:
            logger.error("Order #%s: can't find invoice while assigning order", order.number)
    
    def get_default_partner(self, order):
        # At the moment we assumes that the only partner may have stockreckord
        # so no per-partner invoice splitting  supported yet
        partner_ids = [l['partner_id'] for l in order.lines.values()]
        partner = None
        if len(partner_ids) > 0:
            try:
                partner = Partner.objects.get(pk=partner_ids[0])
            except Partner.DoesNotExist:
                logger.error("Order #%s: cant find fulfillment partner for invoice", order.number)
        
        return partner

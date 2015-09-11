import logging

from decimal import Decimal as D

from oscar.core.loading import get_class, get_model

Partner = get_model('partner', 'Partner')
Person = get_model('oscar_ficta', 'Person')
Invoice = get_model('invoice', 'Invoice')

# Standard logger for checkout events
logger = logging.getLogger('oscar.checkout')

class CheckoutSessionMixin(object):
    """some helpers for managing juristic persons during checkout
    """
    def pay_as_person(self, person_id):
        id = -1
        #  TODO: DRY it!
        if person_id <> -1:
            try:
                person = Person.browsable.get(pk=person_id)
            except Person.DoesNotExist:
                pass
            else:
                id = getattr(person, 'id', -1)
                 
        self.checkout_session._set('payment', 'person', id)
        
    def get_person_id(self):
        return self.checkout_session._get('payment', 'person')
    
    def set_invoice_order(self, order):
        # assigns an order to an invoice 
        # and save invoice in the session 
        invoice = partner = None
        invoices = []
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
                #TODO raise ImproperlyConfigured
                logger.warning("Order #%s: cant find partner's juristic person for invoice", order.number)
                pass
            invoice.order=order
            invoice.status=invoice.NEW
            invoice.save()
            self.checkout_session._set('payment', 'invoice', invoice.number)
        else:
            logger.error("Order #%s: cant find invoice while assigning order", order.number)
    
    def get_default_partner(self, order):
        # At the moment we assumes that the only partner may have stockreckord
        # so no invoice splitting per-partner supported 
        partner_ids = [l['partner_id'] for l in order.lines.values()]
        partner = None
        if len(partner_ids) > 0:
            try:
                partner = Partner.objects.get(pk=partner_ids[0])
            except Partner.DoesNotExist:
                logger.error("Order #%s: cant find fulfillment partner for invoice", order.number)
        
        return partner
         
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_classes, get_class, get_model
from oscar.apps.payment.exceptions import UnableToTakePayment


Person = get_model('oscar_ficta', 'Person')
Invoice = get_model('invoice', 'Invoice')

class InvoiceFacade(object):
    def make_pre_invoice(self, user, order_number, total, person):
        #person_id = None
        # check for invoices being made on prevous steps
        # and failed for some reasons  
        try:
            invoices = list(Invoice.objects.filter(order_number__exact=order_number, 
                                             status__exact=Invoice.DRAFT,
                                             order__exact=None).order_by('-date_created'))
        except Invoice.DoesNotExist:
            pass
        
        if len(invoices) > 0:
            # take the last one if more than one returned
            # TODO: maybe makes sense to cleanup orphaned pre-invoices on this step
            invoice = invoices[0]
        else:
            # or create a new one
            invoice = Invoice()
            
        if isinstance(person, Person):
            invoice.person = person
        #elif isinstance(person, User):
        #    person_id = person.get_full_name() or person.email
        invoice.order_number = order_number
        invoice.total_incl_tax = total.incl_tax
        invoice.total_excl_tax = total.excl_tax
        invoice.currency = total.currency
        invoice.user = user
        invoice.save()
        
        if hasattr(invoice, 'number'):
            return invoice.number
        else:
            msg = _("Can't save invoice for order #%s" % order_number)
            raise UnableToTakePayment(msg) 
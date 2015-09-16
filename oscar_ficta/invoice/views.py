import warnings
import logging

from django.contrib import messages
from django.core.paginator import InvalidPage
from django.utils.http import urlquote
from django.http import HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings

from oscar.core.loading import get_class, get_model
#from oscar.apps.catalogue.signals import product_viewed

Invoice = get_model('invoice', 'Invoice')

countries = getattr(settings, 'OSCAR_FICTA_COUNTRIES', ['RU'])

logger = logging.getLogger('oscar_ficta.invoice')

class InvoiceDetailView(DetailView):
    context_object_name = 'invoice'
    model = Invoice


class InvoicePrintView(DetailView):
    context_object_name = 'invoice'
    model = Invoice
    template_folder = "oscar_ficta/invoice"
    number_url_kwarg = 'number'


    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.

        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by invoice number.
        number = self.kwargs.get(self.number_url_kwarg, None)
        user = self.request.user
        logger.info("Invoice #%s generating started by user #%s", number, user.id)
        if number is not None:
            # TODO: add printable manager
            q_args = {'number' : number,}
            if not user.is_superuser:
                # superuser can print any invoice
                q_args['status__in'] = (Invoice.NEW, Invoice.SENT, Invoice.APPROVED)
            if user.has_perm('partner.dashboard_access') and not user.is_staff:
                # users attached to partner can print any partner's invoice
                # this is depends on business logic
                user_persons = []
                for p in user.partners.values_list():
                    p += p.juristic_persons.values_list()
                q_args['partner_person__in'] = user_persons 
            if not user.is_staff:
                # staff users can print any 
                q_args['user'] = user
            logger.info("QS for invoice #%s: %s", number, q_args)    
            queryset = queryset.filter(**q_args)


        # If none of those are defined, it's an error.
        else:
            raise AttributeError("Invoice print view %s must be called with "
                                 "an invoice number."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            logger.error("Invoice not found #%s: %s", number, q_args)
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj   
    
    def get_context_data(self, **kwargs):
        ctx = super(InvoicePrintView, self).get_context_data(**kwargs)
        ctx['date_printed'] = timezone.now()
        return ctx
    
    def get_template_names(self):
        """
        Return a list of possible templates.

        If an overriding class sets a template name, we use that. Otherwise,
        we try another option before defaulting to oscar_ficta/invoice/print.html:
            1). oscar_ficta/invoice/<COUNTRY_CODE>/print.html
            

        This allows alternative templates to be provided for a per-country basis.
        """
        if self.template_name:
            return [self.template_name]

        return [
            '%s/%s/print.html' % (
                self.template_folder, countries[0].lower()),
            '%s/print.html' % (self.template_folder)]
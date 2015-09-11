import warnings

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

        if number is not None:
            # TODO: add printable manager
            queryset = queryset.filter(number=number, 
                                       status__in=(Invoice.NEW, Invoice.SENT, Invoice.APPROVED))


        # If none of those are defined, it's an error.
        else:
            raise AttributeError("Invoice print view %s must be called with "
                                 "an invoice number."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
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
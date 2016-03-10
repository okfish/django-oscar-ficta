# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from oscar.core.utils import slugify, get_default_currency
from oscar.core.compat import AUTH_USER_MODEL
#from oscar.models.fields import AutoSlugField

from oscar.core.loading import get_classes, get_model, get_class

from .utils import InvoiceNumberGenerator

class AbstractInvoice(models.Model):

    (DRAFT, NEW, SENT, 
     APPROVED, DECLINED, 
     PAID_PARTIAL, PAID_FULL, PAID_OVER,
     OUTDATED, CANCELLED, DELETED) = range(1, 12)
    INVOICE_STATUSES = {
            DRAFT: _("Draft"), # No order assigned, but have an order number
            NEW: _("New"),
            SENT: _("Invoice sent"),
            APPROVED: _("Approved by buyer"),
            DECLINED: _("Declined by buyer"),
            PAID_PARTIAL: _("Invoice paid partially"),
            PAID_FULL: _("Invoice paid fully"),
            PAID_OVER: _("Overpaid"),
            OUTDATED: _("Outdated for payment"),
            CANCELLED: _("Cancelled by manager"),
            DELETED: _("Deleted"),
        }
    
    # Use number instead of PK to make it editable (e.g. for import)
    number = models.CharField(max_length=64, unique=True, null=True)
    
    # Juristic person-partner which recieves a payment
    partner_person = models.ForeignKey(
        'oscar_ficta.Person',
        verbose_name=_("Fulfillment partner"),
        related_name="invoices", null=True,)
    # Order number
    # we store it separately for the first step
    # when no Order is saved but order number has been generated
    order_number = models.CharField(
        _("Order number"), max_length=128, db_index=True)
    # Order to pay for
    # should be assigned after successful order placement
    order =  models.ForeignKey(
        'order.Order', verbose_name=_("Order"), related_name='assigned_invoices',
        null=True, blank=True, on_delete=models.SET_NULL)
    # User-buyer and payer if no person given
    user = models.ForeignKey(
        AUTH_USER_MODEL, related_name='user_invoices', null=True, blank=True,
        verbose_name=_("User"), on_delete=models.SET_NULL)
    
    # Juristic person-payer
    person =  models.ForeignKey(
        'oscar_ficta.Person', related_name='person_invoices', null=True, blank=True,
        verbose_name=_("Juristic person"), on_delete=models.SET_NULL)
    
    status_choices = [(k, v) for k, v in INVOICE_STATUSES.items()]
    status = models.PositiveIntegerField(
        _("Invoice status"),
        choices=status_choices,
        default=DRAFT)
    
    # Optional meta-data about invoice
    merchant_reference = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    
    # Total price looks like it could be calculated by adding up the
    # prices of the associated order, but in some circumstances extra
    # invoice-level charges are added and so we need to store it separately
    currency = models.CharField(
        _("Currency"), max_length=12, default=get_default_currency)
    total_incl_tax = models.DecimalField(
        _("Order total (inc. tax)"), decimal_places=2, max_digits=12)
    total_excl_tax = models.DecimalField(
        _("Order total (excl. tax)"), decimal_places=2, max_digits=12)
    
    
    # Date information
    date_created = models.DateTimeField(
        _("Date created"),
        auto_now_add=True)
    date_updated = models.DateTimeField(
        _("Date updated"),
        auto_now=True,
        db_index=True)

    def current_status(self):
        return self.INVOICE_STATUSES[self.status]
    
    class Meta:
        abstract = True
        ordering = ('-date_created',)
        
    def __unicode__(self):
        return self.number
    
    def save(self, *args, **kwargs):
        # We generate a invoice number using the PK of the invoice so
        # we save the invoice first
        super(AbstractInvoice, self).save(*args, **kwargs)
        if not self.number:
            self.number = self._generate_number()
            super(AbstractInvoice, self).save()
    
    def _generate_number(self):
        obj = InvoiceNumberGenerator().invoice_number(self.order_number, self.id)
        return obj
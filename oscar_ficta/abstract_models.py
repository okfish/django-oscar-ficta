# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.conf import settings

from oscar.core.utils import slugify
from oscar.core.compat import AUTH_USER_MODEL
from oscar.models.fields import AutoSlugField
from oscar.apps.address.abstract_models import AbstractAddress
from oscar.core.loading import get_classes, get_model, get_class


BrowsablePersonManager = get_class(
    'oscar_ficta.managers', 'BrowsablePersonManager')

from internationalflavor.iban import BICField, IBANField

from .fields import VATNumberField


(ACTIVE, LIQUIDATING, LIQUIDATED) = range(1, 4)
PERSON_STATUSES = {
        ACTIVE: _("Active"),
        LIQUIDATING: _("Liquidating process started"),
        LIQUIDATED: _("Liquidated"),
    }

countries = getattr(settings, 'OSCAR_FICTA_COUNTRIES', ['RU'])

class AbstractPersonGroup(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(AbstractPersonGroup, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class AbstractLegalAddress(AbstractAddress):
    person = models.OneToOneField(
        'oscar_ficta.Person',
        verbose_name=_("Juristic person"),
        related_name="legal_address")
    
    class Meta:
        abstract = True
        verbose_name = _("Legal address")
        verbose_name_plural = _("Legal addresses")
        
class AbstractPerson(models.Model):
    
    # As it said in wiki there are too many number formats
    # but no longer than 15 chars (hello, Canada :)
    # see https://en.wikipedia.org/wiki/VAT_identification_number
    # for explanation
    # django-internationalflavor seems to be the right solution
    # for VAT and BIC fields validation
    
    vatin = VATNumberField(countries=countries, 
                           verbose_name=_("VAT number"), 
                           help_text=_("VAT or tax payer ID"),
                           unique=True)
    reason_code = models.CharField(
        _("Code for Reason of registration, e.g. KPP in Russia"), 
        null=True, 
        blank=True, max_length=9)
    name = models.CharField(_('Name'), max_length=200)
    slug = AutoSlugField(_("Code"), max_length=200, unique=True,
                         populate_from='name')
    
    partner = models.ForeignKey(
        'partner.Partner',
        verbose_name=_("Fulfillment partner"),
        related_name="juristic_persons", null=True,)
    
    users = models.ManyToManyField(
        AUTH_USER_MODEL, related_name="related_persons",
        blank=True, verbose_name=_("Users"))
    
    
    # Contact details
    manager_name = models.CharField(
        _('Manager name'), max_length=200, blank=True, null=True)
    chief_name = models.CharField(
        _('GM or Director name'), max_length=200, blank=True, null=True)
    chief_title = models.CharField(
        _('Title for GM or Director'), max_length=200, blank=True, null=True)
    accountant_name = models.CharField(
        _('Main Accountant name'), max_length=200, blank=True, null=True)
    
    phone = models.CharField(_('Phone'), max_length=64, blank=True, null=True)
    email = models.EmailField(_('Email'), max_length=254, blank=True, null=True)

    reference = models.CharField(
        _("Reference"),
        max_length=32,
        unique=True,
        null=True,
        blank=True,
        help_text=_("A reference number that uniquely identifies this person"))

    description = models.TextField(
        _("Description"),
        max_length=2000,
        blank=True, null=True)

    group = models.ForeignKey(
        'oscar_ficta.PersonGroup',
        related_name='persons',
        verbose_name=_("Group"),
        null=True,
        blank=True)
    
    is_active = models.BooleanField(_("Is active"), default=True)
    
    status_choices = [(k, v) for k, v in PERSON_STATUSES.items()]
    status = models.PositiveIntegerField(
        _("State status"),
        choices=status_choices,
        default=ACTIVE)
    
    # Date information
    date_created = models.DateTimeField(
        _("Date created"),
        auto_now_add=True)
    date_updated = models.DateTimeField(
        _("Date updated"),
        auto_now=True,
        db_index=True)
    date_registration = models.DateTimeField(
        _("Date of registration"),
        blank=True, null=True)
    date_liquidation = models.DateTimeField(
        _("Date of liquidation"),
        blank=True, null=True)
    
    browsable = BrowsablePersonManager()
    objects = models.Manager()

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
        verbose_name = _("Juristic person")
        verbose_name_plural = _("Juristic persons")
        unique_together = ("vatin", "reason_code")


class AbstractBankAccount(models.Model):
    person = models.ForeignKey(
        'oscar_ficta.Person',
        verbose_name=_("Owner's juristic person"),
        related_name="bank_accounts")
    bank = models.ForeignKey(
        'oscar_ficta.Bank',
        verbose_name=_("Bank"),
        related_name="person_accounts")
    iban = IBANField(_("IBAN"), blank=True, null=True, unique=True)
    settlement_account = models.CharField(
        _("Settlement account number"), max_length=20)

    is_active = models.BooleanField(_("Is active"), default=True)
    is_default = models.BooleanField(_("Use it by default?"), default=True)
    
    class Meta:
        abstract = True
        verbose_name = _("Bank account")
        verbose_name_plural = _("Bank accounts")
        unique_together = ("bank", "settlement_account")


class AbstractBank(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    bic = BICField(_("BIC"))
    swift = models.CharField(_('SWIFT code'), max_length=11, blank=True, null=True, unique=True)    
    correspondent_account = models.CharField(
        _("Correspondent account number"), max_length=20)
    person = models.OneToOneField(
        'oscar_ficta.Person',
        verbose_name=_("Juristic person"),
        related_name="banks",
        null=True, 
        blank=True,)

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")
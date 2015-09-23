from decimal import Decimal as D

from django import forms
from django.conf import settings
from django.core import exceptions
from django.http import QueryDict
from django.utils.translation import ugettext_lazy as _
from django.db.models import get_model
from django.forms.models import inlineformset_factory

from treebeard.forms import movenodeform_factory

from oscar.forms.widgets import DatePickerInput
from oscar.templatetags.currency_filters import currency

PersonGroup = get_model('oscar_ficta', 'PersonGroup')
Person = get_model('oscar_ficta', 'Person')
LegalAddress = get_model('oscar_ficta', 'LegalAddress')
BankAccount = get_model('oscar_ficta', 'BankAccount')
Bank = get_model('oscar_ficta', 'Bank')

Invoice = get_model('invoice', 'Invoice')


GroupForm = movenodeform_factory(
    PersonGroup,
    fields=['name', 'description', 'image'])

class PersonSearchForm(forms.Form):
    name = forms.CharField(label=_("Title or name"), required=False)
    vatin = forms.CharField(label=_("VAT number"), required=False)
    status = forms.ChoiceField(label=_("State status"), choices=Person.status_choices, required=False)
    
class NewPersonForm(forms.ModelForm):
#     name = forms.CharField(label=_('Name or title'), max_length=200)
#     vatin = VATNumberFormField(countries=countries, 
#                            label=_("VAT number"), 
#                            help_text=_("VAT or tax payer ID"))
#     reason_code = forms.CharField(
#         label=_("Code for Reason of registration, e.g. KPP in Russia"), 
#         max_length=9, required=False)
    
    def __init__(self, *args, **kwargs):
        super(NewPersonForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
    
    class Meta:
        model = Person
        fields = ('name', 'vatin', 'reason_code')
        

class UpdatePersonForm(forms.ModelForm):
    name = forms.CharField(label=_("Name"), required=True)

#    def __init__(self, *args, **kwargs):
#        super(UpdatePersonForm, self).__init__(*args, **kwargs)
        

    class Meta:
        model = Person
        fields = [ 'name', 'vatin', 'reason_code', 'group','logo' , 'image',
                  'manager_name', 'chief_title', 'chief_name', 'accountant_name',
                  'phone', 'email', 'partner']

class LegalAddressForm(forms.ModelForm):



    class Meta:
        model = LegalAddress
        fields = ['country', 'postcode', 'line4', 
                  'line1', 'line2', 'line3', ]

class BankAccountForm(forms.ModelForm):

    class Meta:
        model = BankAccount
        fields = ['bank', 'settlement_account', 'is_default']
 
    def __init__(self, *args, **kwargs):
        super(BankAccountForm, self).__init__(*args, **kwargs)
        self.fields['bank'].required = False
        #self.fields['settlement_account'].required = False
    
    # workaround to set required bank field which is not submitted
    # in case of new bank creation
    # http://stackoverflow.com/a/16603803
    def set_bank(self, bank):
        data = self.data.copy()
        data[self.add_prefix('bank')] = bank
        self.data = data

class BankForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BankForm, self).__init__(*args, **kwargs)
        self.fields['bic'].required = False
        self.fields['name'].required = False
        self.fields['correspondent_account'].required = False

    class Meta:
        model = Bank
        fields = ['bic', 'name', 'location', 'correspondent_account']


BankAccountFormSet = inlineformset_factory(
    Person, BankAccount,  form=BankAccountForm,
    extra=1, fk_name="person")

LegalAddressFormSet = inlineformset_factory(
    Person, LegalAddress,  form=LegalAddressForm,
    extra=1, fk_name="person")


# Three forms below proudly stolen from django-oscar-accounts package       
class ChangeStatusForm(forms.ModelForm):
    is_active = forms.BooleanField(widget=forms.widgets.HiddenInput)
    new_status = None

    def __init__(self, *args, **kwargs):
        kwargs['initial']['is_active'] = self.new_status
        super(ChangeStatusForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].required = False

    class Meta:
        model = Person
        fields = ['is_active',]

class FreezePersonForm(ChangeStatusForm):
    new_status = False

class EnablePersonForm(ChangeStatusForm):
    new_status = True


class InvoiceSearchForm(forms.Form):
    invoice_number = forms.CharField(required=False, label=_("Invoice number"))
    name = forms.CharField(required=False, label=_("Customer name"))
    person_name = forms.CharField(required=False, label=_("Juristic person name"))
    status_choices = (('', '---------'),) + tuple(Invoice.status_choices)
    status = forms.ChoiceField(choices=status_choices, label=_("Status"),
                               required=False)

    date_from = forms.DateField(
        required=False, label=_("Date from"), widget=DatePickerInput)
    date_to = forms.DateField(
        required=False, label=_("Date to"), widget=DatePickerInput)

    vatin = forms.CharField(
        label=_("VAT number"), required=False)

    format_choices = (('html', _('HTML')),
                      ('csv', _('CSV')),)
    response_format = forms.ChoiceField(widget=forms.RadioSelect,
                                        required=False, choices=format_choices,
                                        initial='html',
                                        label=_("Get results as"))

    def __init__(self, *args, **kwargs):
        # Ensure that 'response_format' is always set
        if 'data' in kwargs:
            data = kwargs['data']
            del(kwargs['data'])
        elif len(args) > 0:
            data = args[0]
            args = args[1:]
        else:
            data = None

        if data:
            if data.get('response_format', None) not in self.format_choices:
                # Handle POST/GET dictionaries, which are unmutable.
                if isinstance(data, QueryDict):
                    data = data.dict()
                data['response_format'] = 'html'

        super(InvoiceSearchForm, self).__init__(data, *args, **kwargs)

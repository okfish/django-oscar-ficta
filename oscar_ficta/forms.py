# -*- coding: utf-8 -*-
from django import forms
from django.forms import models as modelforms
from django.forms.widgets import RadioSelect
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from oscar.core.loading import get_classes, get_model

from .widgets import PersonRemoteSelect
from .fields import VATNumberFormField

countries = getattr(settings, 'OSCAR_FICTA_COUNTRIES', ['RU'])


def get_persons_choices(user):
    """Returns juristic persons related to given user.
        TODO: add user themself as first person 
        to enable invoicing for a physical persons too
    """
    full_name = user.get_full_name() or "%s(%s)" % (user.username, user.email) 
    
    persons = [(-1, full_name)]
    if not user.related_persons:
        return persons
    if len(user.related_persons.values_list()) > 0:
        return persons + [(p['id'], p['name']) for p in user.related_persons.values()]
    else:
        return persons


class LegalAddressForm(modelforms.ModelForm):

    class Meta:
        model = get_model('oscar_ficta', 'LegalAddress')
        exclude = ('title', 'first_name', 'last_name', 'search_text')


class PersonForm(forms.Form):
    name = forms.CharField(label=_('Name or title'), max_length=200)
    vatin = VATNumberFormField(countries=countries, 
                               label=_("VAT number"),
                               help_text=_("VAT or tax payer ID"))
    reason_code = forms.CharField(
        label=_("Code for Reason of registration, e.g. KPP in Russia"), 
        max_length=9, required=False)


class PersonSelectForm(forms.Form):
    
    person = forms.IntegerField(widget=forms.HiddenInput, required=False)
     
    def __init__(self, *args, **kwargs):
        for_user = None
        default_person = None
        choices = None
        label = _("Juristic persons list")
        help_text = _("Select a company from the list or <a href='{% url 'customer:person-create' %}' data-toggle='tooltip' title='Create a new juristic person'>add a new</a>")
        if 'for_user' in kwargs.keys():
            for_user = kwargs.pop('for_user')
            widget = forms.HiddenInput
            choices = get_persons_choices(for_user)
            if not choices is None and len(choices) > 0:
                widget=RadioSelect
            else:
                label = _("No juristic persons found")
                
        else:
            # if no user given renders Select2 widget 
            # full list of persons will be used
            widget = PersonRemoteSelect
            label = _("All available persons")
            help_text = _("active juristic persons")
            
        if 'default_person' in kwargs.keys():
            default_person = kwargs.pop('default_person')
            
        super(PersonSelectForm, self).__init__(*args, **kwargs)
        
        if for_user:
            self.fields['person'] = forms.ChoiceField(label=label,
                                                      initial=default_person,
                                                      required=False,
                                                      choices=choices,
                                                      widget=widget,
                                                      help_text=help_text)
        else:
            
            self.fields['person'] = forms.CharField(label=label,
                                                    widget=widget,
                                                    help_text=help_text)

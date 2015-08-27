from django import forms
from django.forms import models as modelforms
from django.forms.widgets import RadioSelect
#from django.db.models import Q, get_model

from oscar.core.loading import get_classes, get_model
from .widgets import PersonRemoteSelect
 
class LegalAddressForm(modelforms.ModelForm):

    class Meta:
        model = get_model('oscar_ficta', 'LegalAddress')
        exclude = ('title', 'first_name', 'last_name', 'search_text')

class PersonForm(modelforms.ModelForm):
    class Meta:
        model = get_model('oscar_ficta', 'Person')
        fields = ('name', 'vatin', 'reason_code')
        #exclude = ('code', 'users', 'partner', 'description', 'reference'
        #           'date_created', 'date_updated', 'group')
        
class PersonSelectForm(forms.Form):
    
    person = forms.IntegerField(widget=forms.HiddenInput)
     
    def __init__(self, *args, **kwargs):
        model = get_model('oscar_ficta', 'Person')
        
        if 'for_user' in kwargs.keys():
            for_user = kwargs.pop('for_user')
            widget=RadioSelect
        else:
            # if no user given renders Select2 widget 
            # full list of persons will be used
            widget=PersonRemoteSelect
            
        if 'default_person' in kwargs.keys():
            default_person = kwargs.pop('default_person')
            
        super(PersonSelectForm, self).__init__(*args, **kwargs)
        choices = None
        self.fields['person'] = forms.ChoiceField(label=_("Available juristic persons"),
                                choices=choices,
                                default=default_person,
                                widget=widget,)
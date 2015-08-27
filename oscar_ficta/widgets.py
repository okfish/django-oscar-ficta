from django.core.urlresolvers import reverse_lazy
from django import forms

from oscar.forms.widgets import RemoteSelect

class PersonRemoteSelect(RemoteSelect):
    """
    PEC city code selector based on Select2 widget.
    
    """
    lookup_url = reverse_lazy('oscar_ficta:person-lookup', 
                              #kwargs={'slug' : 'pek'}
                              )

    def __init__(self, *args, **kwargs):
        super(PecomCitySelect, self).__init__(*args, **kwargs)
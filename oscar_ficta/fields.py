import re

from django.conf import settings

from internationalflavor.vat_number import VATNumberField as OriginalVATNumberField
from internationalflavor.vat_number import VATNumberFormField as OriginalVATNumberFormField

default_country = 'RU'
countries = getattr(settings, 'OSCAR_FICTA_COUNTRIES', [])
if countries:
    default_country = countries[0].upper()

class VATNumberField(OriginalVATNumberField):
    """  Wrap internationalflavors VATNumberField to support
        numbers without country prefix.
        Appends default country prefix specified in the settings
        OSCAR_FICTA_COUNTRIES[0]
    """
    def to_python(self, value):
        value = super(VATNumberField, self).to_python(value)
        if value is not None:
            if not re.match(r"^[A-Z]{2}[A-Z0-9]+$", value):
                # Trying add default country
                return default_country + value
        return value
    
    def formfield(self, **kwargs):
        defaults = {'form_class': VATNumberFormField}
        defaults.update(kwargs)
        return super(VATNumberField, self).formfield(**defaults)
    
    
class VATNumberFormField(OriginalVATNumberFormField):
    
    def to_python(self, value):
        value = super(VATNumberFormField, self).to_python(value)
        if value is not None:
            if not re.match(r"^[A-Z]{2}[A-Z0-9]+$", value):
                # Trying add default country
                return default_country + value
        return value
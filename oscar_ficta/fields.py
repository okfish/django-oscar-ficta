import re

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from internationalflavor.vat_number import VATNumberField as OriginalVATNumberField
from internationalflavor.vat_number import VATNumberFormField as OriginalVATNumberFormField
from internationalflavor.iban import BICField as OriginalBICField
from internationalflavor.iban import BICFormField as OriginalBICFormField

from oscar.core.loading import get_classes, get_model, get_class

#BICValidator = get_class('oscar_ficta.validators', 'BICValidator')
from oscar_ficta.validators import BICValidator
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
    
    def get_prep_value(self, value):
        value = super(VATNumberField, self).get_prep_value(value)
        if value is not None:
            if re.match(r"^[A-Z]{2}[A-Z0-9]+$", value):
                # Trying delete default country code from value
                country, rest = value[0:2], value[2:]
                if country == default_country:
                    return rest
        return value
    
class VATNumberFormField(OriginalVATNumberFormField):
    
    def to_python(self, value):
        value = super(VATNumberFormField, self).to_python(value)
        if value is not None:
            if not re.match(r"^[A-Z]{2}[A-Z0-9]+$", value):
                # Trying add default country
                return default_country + value
        return value
    
    def get_prep_value(self, value):
        value = super(VATNumberField, self).get_prep_value(value)
        if value is not None:
            if re.match(r"^[A-Z]{2}[A-Z0-9]+$", value):
                # Trying delete default country code from value
                country, rest = value[0:2], value[2:]
                if country == default_country:
                    return rest
        return value    
    
    
class BICFormField(OriginalBICFormField):
    """A form field that applies the :class:`.validators.BICValidator`."""

    def __init__(self, *args, **kwargs):
        self.default_validators = [BICValidator()]
        super(OriginalBICFormField, self).__init__(*args, **kwargs)
        
class BICField(OriginalBICField):
    """A model field that applies the :class:`.validators.BICValidator` and is represented by a
    :class:`.forms.BICFormField`.

    This field is an extension of a CharField.
    """

    description = _('An International Bank Code')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 11)
        super(OriginalBICField, self).__init__(*args, **kwargs)
        self.validators.append(BICValidator())  # pylint: disable=E1101
        
    def formfield(self, **kwargs):
        defaults = {'form_class': BICFormField}
        defaults.update(kwargs)
        return super(OriginalBICField, self).formfield(**defaults)
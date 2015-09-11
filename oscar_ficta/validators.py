# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.six.moves.urllib import request

from internationalflavor.iban import BICValidator as OriginalBICValidator

default_country = None
countries = getattr(settings, 'OSCAR_FICTA_COUNTRIES', [])
if countries:
    default_country = countries[0].upper()

logger = logging.getLogger('oscar.checkout')

# Customize original validator to make local BIC validation
# if no localized validators found - fall back into superclass
class BICValidator(OriginalBICValidator):
    def __call__(self, value):
        default_country = None
        countries = getattr(settings, 'OSCAR_FICTA_COUNTRIES', [])
        if countries:
            default_country = countries[0].upper()
        logger.info("BIC #%s country %s", value, default_country)
        if default_country == 'RU':
            return self._validate_ru_bic(value)
        else:
            super(BICValidator, self).__call__(value)
    
    def _validate_ru_bic(self, value):
        # this regex proudly stolen from pytalk.ru forum
        # see http://pytalk.ru/forum/django/20648/
        # seems not to be full as wiki says
        # https://ru.wikipedia.org/wiki/%D0%91%D0%B0%D0%BD%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%B8%D0%B4%D0%B5%D0%BD%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B9_%D0%BA%D0%BE%D0%B4
      
        err_msg = _("This Bank Identifier Code (BIC #%s) is not valid for Russia." % value)
        if not re.match("^[0-9]{9}$", value):
            raise ValidationError(err_msg)
        prefix = value[:2]
        if prefix != '04':
            err_msg = "%s\n%s%s." % (err_msg, _("First 2 digits should be Russian Federation code (04). Used: "), prefix)
            raise ValidationError(err_msg)
        cre_num = int(value[6:9])
        if not (50 <= cre_num <= 999):
            err_msg = "%s\n%s%s" % (err_msg, _("Invalid credit organisation number:"), cre_num)
            raise ValidationError(err_msg)
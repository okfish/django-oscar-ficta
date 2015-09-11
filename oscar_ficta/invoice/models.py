# -*- coding: utf-8 -*-
from oscar.core.loading import is_model_registered
from oscar_ficta.invoice.abstract_models import (
    AbstractInvoice, 
    )

__all__ = []


if not is_model_registered('oscar_ficta.invoice', 'Invoice'):
    class Invoice(AbstractInvoice):
        pass

    __all__.append('Invoice')
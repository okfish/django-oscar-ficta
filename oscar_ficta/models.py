# -*- coding: utf-8 -*-
from oscar.core.loading import is_model_registered
from oscar_ficta.abstract_models import (
    AbstractPersonGroup, 
    AbstractLegalAddress, 
    AbstractPerson, 
    AbstractBankAccount, 
    AbstractBank)

__all__ = []


if not is_model_registered('oscar_ficta', 'PersonGroup'):
    class PersonGroup(AbstractPersonGroup):
        pass

    __all__.append('PersonGroup')


if not is_model_registered('oscar_ficta', 'LegalAddress'):
    class LegalAddress(AbstractLegalAddress):
        pass

    __all__.append('LegalAddress')
    

if not is_model_registered('oscar_ficta', 'Person'):
    class Person(AbstractPerson):
        pass

    __all__.append('Person')
    

if not is_model_registered('oscar_ficta', 'BankAccount'):
    class BankAccount(AbstractBankAccount):
        pass

    __all__.append('BankAccount')


if not is_model_registered('oscar_ficta', 'Bank'):
    class Bank(AbstractBank):
        pass

    __all__.append('Bank')
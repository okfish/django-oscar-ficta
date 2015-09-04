from decimal import Decimal as D

from oscar.core.loading import get_class, get_model

Person = get_model('oscar_ficta', 'Person')

class CheckoutSessionMixin(object):
    """some helpers for managing juristic persons during checkout
    """
    def pay_as_person(self, person_id):
        person = Person.browsable.get(pk=person_id)
        if person:
            self.checkout_session._set('payment', 'person', person.id)
        
    def get_person_id(self):
        return self.checkout_session._get('payment', 'person')
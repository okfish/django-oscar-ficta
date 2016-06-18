from oscar.core.loading import get_class, get_model
from oscar.core.exceptions import (
    AppNotFoundError, ClassNotFoundError, ModuleNotFoundError)

try:
    UserSessionData = get_class(
        'user.session', 'UserSessionData')
except (ImportError, AppNotFoundError, ClassNotFoundError, ModuleNotFoundError):
    from .checkout.session import FictaSessionData as UserSessionData

Person = get_model('oscar_ficta', 'Person')


def current_person(request):
    ctx = {}
    if getattr(request, 'user', None) and request.user.is_authenticated():
        user = request.user
        user_session = UserSessionData(request)
        person_id = user_session.get_person_id()
        if person_id == -1:
            person = -1
        # current_person is None when no linked persons found
        else:
            person = None
        if user.related_persons and len(user.related_persons.values_list()) > 0:
            try:
                person = user.related_persons.get(pk=person_id)
            except Person.DoesNotExist:
                # set current person to -1 that points to user themselves
                person = -1
        ctx = {'current_person': person}
    return ctx

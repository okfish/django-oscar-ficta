from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OscarFictaConfig(AppConfig):
    label = 'oscar_ficta'
    name = 'oscar_ficta'
    verbose_name = _('Persona Ficta for Oscar')


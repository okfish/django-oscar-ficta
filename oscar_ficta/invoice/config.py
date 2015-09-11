from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OscarFictaInvoiceConfig(AppConfig):
    label = 'invoice'
    name = 'oscar_ficta.invoice'
    verbose_name = _('Payment via Invoice for Oscar')

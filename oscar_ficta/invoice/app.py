from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

from oscar.core.application import Application

from oscar_ficta.invoice import views


class InvoiceApplication(Application):
    name = 'invoice'
    print_view = views.InvoicePrintView
    detail_view = views.InvoiceDetailView
    permissions_map = {
        'detail': (['is_staff'], ['partner.dashboard_access']),
    }

    
    def get_urls(self):
        urlpatterns = super(InvoiceApplication, self).get_urls()
        urlpatterns += patterns('',
            url(r'^print/(?P<number>[\w-]+)/$', self.print_view.as_view(),
                name='print'),
            url(r'^view/(?P<pk>\d+)/$',
                self.detail_view.as_view(), name='detail'),
        )
#         urlpatterns += patterns('',
#             url(r'^person-lookup/', cache_page(60*10)(self.person_lookup_view.as_view()),
#                 name='person-lookup'),
#         )
        return self.post_process_urls(urlpatterns)


application = InvoiceApplication()
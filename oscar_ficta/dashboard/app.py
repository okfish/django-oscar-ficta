from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required

from oscar.core.application import Application
from oscar.core.loading import get_class


class FictaDashboardApplication(Application):
    name = 'oscar_ficta_dashboard'
    default_permissions = ['is_staff', ]
    
    person_list_view = get_class('oscar_ficta.dashboard.views', 'PersonListView')
    person_create_view = get_class('oscar_ficta.dashboard.views', 'PersonCreateView')
    person_update_view = get_class('oscar_ficta.dashboard.views', 'PersonUpdateView')
    person_detail_view = get_class('oscar_ficta.dashboard.views', 'PersonDetailView')
    person_freeze_view = get_class('oscar_ficta.dashboard.views', 'PersonFreezeView')
    person_enable_view = get_class('oscar_ficta.dashboard.views', 'PersonEnableView')
    
    group_list_view = get_class('oscar_ficta.dashboard.views',
                                   'GroupListView')
    group_detail_list_view = get_class('oscar_ficta.dashboard.views',
                                          'GroupDetailListView')
    group_create_view = get_class('oscar_ficta.dashboard.views',
                                     'GroupCreateView')
    group_update_view = get_class('oscar_ficta.dashboard.views',
                                     'GroupUpdateView')
    group_delete_view = get_class('oscar_ficta.dashboard.views',
                                     'GroupDeleteView')
    
    invoice_list_view = get_class('oscar_ficta.dashboard.views', 'InvoiceListView')
#     account_top_up_view = views.AccountTopUpView
# 
#     transfer_list_view = views.TransferListView
#     transfer_detail_view = views.TransferDetailView
# 
#     report_deferred_income = views.DeferredIncomeReportView
#     report_profit_loss = views.ProfitLossReportView

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$',
                self.person_list_view.as_view(),
                name='persons-list'),
            url(r'^create/$', self.person_create_view.as_view(),
                name='persons-create'),
            url(r'^(?P<pk>\d+)/update/$', self.person_update_view.as_view(),
                 name='persons-update'),
             url(r'^(?P<pk>\d+)/$', self.person_detail_view.as_view(),
                 name='persons-detail'),
            url(r'^(?P<pk>\d+)/freeze/$', self.person_freeze_view.as_view(),
                name='persons-freeze'),
            url(r'^(?P<pk>\d+)/enable/$', self.person_enable_view.as_view(),
                name='persons-enable'),
                               
            url(r'^groups/$', self.group_list_view.as_view(),
                name='group-list'),
            url(r'^groups/(?P<pk>\d+)/$',
                self.group_detail_list_view.as_view(),
                name='group-detail-list'),
            url(r'^groups/create/$', self.group_create_view.as_view(),
                name='group-create'),
            url(r'^groups/create/(?P<parent>\d+)$',
                self.group_create_view.as_view(),
                name='group-create-child'),
            url(r'^groups/(?P<pk>\d+)/update/$',
                self.group_update_view.as_view(),
                name='group-update'),
            url(r'^groups/(?P<pk>\d+)/delete/$',
                self.group_delete_view.as_view(),
                name='group-delete'),                               
                               
            url(r'^invoices/$', self.invoice_list_view.as_view(), name='invoice-list'),
        )
        return self.post_process_urls(urlpatterns)


application = FictaDashboardApplication()
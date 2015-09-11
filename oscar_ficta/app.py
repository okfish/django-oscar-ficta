from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

from oscar.core.application import Application

from oscar_ficta import views


class FictaApplication(Application):
    name = 'oscar_ficta'
    select_view = views.PersonSelectView
    detail_view = views.PersonDetailView
    group_view = views.PersonGroupView
    person_lookup_view = views.PersonLookupView
    permissions_map = {
        'index': (['is_staff'], ['partner.dashboard_access']),
        'group': (['is_staff'], ['partner.dashboard_access']),
    }

    
    def get_urls(self):
        urlpatterns = super(FictaApplication, self).get_urls()
        urlpatterns += patterns('',
            url(r'^select/', self.select_view.as_view(),
                name='select'),
            url(r'^(?P<dummyslug>[\w-]+)/(?P<pk>\d+)/$',
                self.detail_view.as_view(), name='detail'),
            url(r'^group/(?P<slug>[\w-]+)/$',
                self.group_view.as_view(), name='group'),
        )
        urlpatterns += patterns('',
            url(r'^person-lookup/', cache_page(60*10)(self.person_lookup_view.as_view()),
                name='person-lookup'),
        )
        return self.post_process_urls(urlpatterns)


application = FictaApplication()
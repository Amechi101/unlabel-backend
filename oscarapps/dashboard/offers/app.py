from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class
from oscar.apps.dashboard.offers.app import OffersDashboardApplication as CoreOffersDashboardApplication

class OffersDashboardApplication(CoreOffersDashboardApplication):
    permissions_map = _map = {
        'offer-list': (['is_staff'], ['partner.dashboard_access']),
        'offer-metadata': (['is_staff'], ['partner.dashboard_access']),
        'offer-condition': (['is_staff'], ['partner.dashboard_access']),
        'offer-benefit': (['is_staff'], ['partner.dashboard_access']),
        'offer-restrictions': (['is_staff'], ['partner.dashboard_access']),
        'offer-delete': (['is_staff'], ['partner.dashboard_access']),
        'offer-detail': (['is_staff'], ['partner.dashboard_access']),

    }



    def get_urls(self):
        urls = [
            url(r'^$', self.list_view.as_view(), name='offer-list'),
            # Creation
            url(r'^new/name-and-description/$', self.metadata_view.as_view(),
                name='offer-metadata'),
            url(r'^new/condition/$', self.condition_view.as_view(),
                name='offer-condition'),
            url(r'^new/incentive/$', self.benefit_view.as_view(),
                name='offer-benefit'),
            url(r'^new/restrictions/$', self.restrictions_view.as_view(),
                name='offer-restrictions'),
            # Update
            url(r'^(?P<pk>\d+)/name-and-description/$',
                self.metadata_view.as_view(update=True),
                name='offer-metadata'),
            url(r'^(?P<pk>\d+)/condition/$',
                self.condition_view.as_view(update=True),
                name='offer-condition'),
            url(r'^(?P<pk>\d+)/incentive/$',
                self.benefit_view.as_view(update=True),
                name='offer-benefit'),
            url(r'^(?P<pk>\d+)/restrictions/$',
                self.restrictions_view.as_view(update=True),
                name='offer-restrictions'),
            # Delete
            url(r'^(?P<pk>\d+)/delete/$',
                self.delete_view.as_view(), name='offer-delete'),
            # Stats
            url(r'^(?P<pk>\d+)/$', self.detail_view.as_view(),
                name='offer-detail'),
        ]
        return self.post_process_urls(urls)


application = OffersDashboardApplication()

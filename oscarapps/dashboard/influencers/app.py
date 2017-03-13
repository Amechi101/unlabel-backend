from django.conf.urls import url

from oscar.apps.dashboard.partners.app import PartnersDashboardApplication as CorePartnersDashboardApplication
from oscar.core.loading import get_class


class InfluencersDashboardApplication(CorePartnersDashboardApplication):
    permissions_map = {
        'index': (['is_staff'], ['partner.dashboard_access']),
    }

    influencer_list_view = get_class('oscarapps.dashboard.influencers.views',
                                 'InfluencerListView')
    influencer_create_view = get_class('oscarapps.dashboard.influencers.views',
                                 'InfluencerCreateView')
    influencer_manage_view = get_class('oscarapps.dashboard.influencers.views',
                                 'InfluencerManageView')
    influencer_delete_view = get_class('oscarapps.dashboard.influencers.views',
                                 'InfluencerDeleteView')
    influencer_filter_view = get_class('oscarapps.dashboard.influencers.views',
                                 'InfluencerFilterView')
    user_update_view = get_class('dashboard.influencers.views',
                                 'InfluencerUserUpdateView')

    location_list_view = get_class('oscarapps.dashboard.influencers.views',
                                 'LocationListView')
    location_create_view = get_class('oscarapps.dashboard.influencers.views',
                                 'LocationCreateView')
    location_manage_view = get_class('oscarapps.dashboard.influencers.views',
                                 'LocationManageView')
    location_delete_view = get_class('oscarapps.dashboard.influencers.views',
                                 'LocationDeleteView')


    def get_urls(self):
        urls = [
            url(r'^$', self.influencer_list_view.as_view(), name='influencer-list'),
            url(r'^create/$', self.influencer_create_view.as_view(),
                name='influencer-create'),
            url(r'^(?P<pk>\d+)/$', self.influencer_manage_view.as_view(),
                name='influencer-manage'),
            url(r'^(?P<pk>\d+)/delete/$', self.influencer_delete_view.as_view(),
                name='influencer-delete'),
            url(r'^filter/$', self.influencer_filter_view.as_view(), name='influencer-filter'),
            url(r'^(?P<influencer_pk>\d+)/users/(?P<user_pk>\d+)/update/$',
                self.user_update_view.as_view(),
                name='influencer-user-update'),

            url(r'^location$', self.location_list_view.as_view(), name='location-list'),
            url(r'^location/create/$', self.location_create_view.as_view(),
                name='location-create'),
            url(r'^location/(?P<pk>\d+)/$', self.location_manage_view.as_view(),
                name='location-manage'),
            url(r'^location/(?P<pk>\d+)/delete/$', self.location_delete_view.as_view(),
                name='location-delete'),
        ]
        return self.post_process_urls(urls)
application = InfluencersDashboardApplication()
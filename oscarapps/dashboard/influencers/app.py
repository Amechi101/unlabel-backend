from oscar.apps.dashboard.partners.app import PartnersDashboardApplication as CorePartnersDashboardApplication
from django.conf.urls import url
from oscar.core.loading import get_class

class InfluencersDashboardApplication(CorePartnersDashboardApplication):

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


    user_link_view = get_class('dashboard.influencers.views',
                               'InfluencerUserLinkView')
    user_unlink_view = get_class('dashboard.influencers.views',
                                 'InfluencerUserUnlinkView')
    user_create_view = get_class('dashboard.influencers.views',
                                 'InfluencerUserCreateView')
    user_select_view = get_class('dashboard.influencers.views',
                                 'InfluencerUserSelectView')
    user_update_view = get_class('dashboard.influencers.views',
                                 'InfluencerUserUpdateView')



    def get_urls(self):
        urls = [

            url(r'^$', self.influencer_list_view.as_view(), name='influencer-list'),
            url(r'^create/$', self.influencer_create_view.as_view(),
                name='influencer-create'),
            url(r'^(?P<pk>\d+)/$', self.influencer_manage_view.as_view(),
                name='influencer-manage'),
            url(r'^(?P<pk>\d+)/delete/$', self.influencer_delete_view.as_view(),
                name='influencer-delete'),


            url(r'^(?P<influencer_pk>\d+)/users/add/$',
                self.user_create_view.as_view(),
                name='influencer-user-create'),
            url(r'^(?P<influencer_pk>\d+)/users/select/$',
                self.user_select_view.as_view(),
                name='influencer-user-select'),
            url(r'^(?P<influencer_pk>\d+)/users/(?P<user_pk>\d+)/link/$',
                self.user_link_view.as_view(), name='influencer-user-link'),
            url(r'^(?P<influencer_pk>\d+)/users/(?P<user_pk>\d+)/unlink/$',
                self.user_unlink_view.as_view(), name='influencer-user-unlink'),
            url(r'^(?P<influencer_pk>\d+)/users/(?P<user_pk>\d+)/update/$',
                self.user_update_view.as_view(),
                name='influencer-user-update'),

            url(r'^filter/$', self.influencer_filter_view.as_view(), name='influencer-filter'),
        ]
        return self.post_process_urls(urls)
application = InfluencersDashboardApplication()
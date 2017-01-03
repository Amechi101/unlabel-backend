from oscar.apps.dashboard.partners.app import PartnersDashboardApplication as CorePartnersDashboardApplication
from django.conf.urls import url
from oscar.core.loading import get_class
class PartnersDashboardApplication(CorePartnersDashboardApplication):

    partner_address_manage_view = get_class('oscarapps.dashboard.partners.views', 'PartnerAddressManageView')

    influencer_list_view = get_class('oscarapps.dashboard.partners.views',
                                 'InfluencerListView')

    influencer_create_view = get_class('oscarapps.dashboard.partners.views',
                                 'InfluencerCreateView')
    influencer_manage_view = get_class('oscarapps.dashboard.partners.views',
                                 'InfluencerManageView')
    influencer_delete_view = get_class('oscarapps.dashboard.partners.views',
                                 'InfluencerDeleteView')


    user_link_view = get_class('dashboard.partners.views',
                               'InfluencerUserLinkView')
    user_unlink_view = get_class('dashboard.partners.views',
                                 'InfluencerUserUnlinkView')
    user_create_view = get_class('dashboard.partners.views',
                                 'InfluencerUserCreateView')
    user_select_view = get_class('dashboard.partners.views',
                                 'InfluencerUserSelectView')
    user_update_view = get_class('dashboard.partners.views',
                                 'InfluencerUserUpdateView')




    industry_preference_list_view = get_class('oscarapps.dashboard.partners.views',
                                 'IndustryListView')

    industry_preference_create_view = get_class('oscarapps.dashboard.partners.views',
                                 'IndustryCreateView')
    industry_preference_manage_view = get_class('oscarapps.dashboard.partners.views',
                                 'IndustryManageView')
    industry_preference_delete_view = get_class('oscarapps.dashboard.partners.views',
                                 'IndustryDeleteView')

    def get_urls(self):
        urls = [
            url(r'^$', self.list_view.as_view(), name='partner-list'),
            url(r'^create/$', self.create_view.as_view(),
                name='partner-create'),
            url(r'^(?P<pk>\d+)/$', self.manage_view.as_view(),
                name='partner-manage'),
            url(r'^(?P<pk>\d+)/delete/$', self.delete_view.as_view(),
                name='partner-delete'),

            url(r'^(?P<pk>\d+)/address/$',
                self.partner_address_manage_view.as_view(),
                name='partner-address-manage'),

            url(r'^(?P<partner_pk>\d+)/users/add/$',
                self.user_create_view.as_view(),
                name='partner-user-create'),
            url(r'^(?P<partner_pk>\d+)/users/select/$',
                self.user_select_view.as_view(),
                name='partner-user-select'),
            url(r'^(?P<partner_pk>\d+)/users/(?P<user_pk>\d+)/link/$',
                self.user_link_view.as_view(), name='partner-user-link'),
            url(r'^(?P<partner_pk>\d+)/users/(?P<user_pk>\d+)/unlink/$',
                self.user_unlink_view.as_view(), name='partner-user-unlink'),
            url(r'^(?P<partner_pk>\d+)/users/(?P<user_pk>\d+)/update/$',
                self.user_update_view.as_view(),
                name='partner-user-update'),



            url(r'^influencer/$', self.influencer_list_view.as_view(), name='influencer-list'),
            url(r'^influencer/create/$', self.influencer_create_view.as_view(),
                name='influencer-create'),
            url(r'^influencer/(?P<pk>\d+)/$', self.influencer_manage_view.as_view(),
                name='influencer-manage'),
            url(r'^influencer/(?P<pk>\d+)/delete/$', self.influencer_delete_view.as_view(),
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



            url(r'^industry_preference/$', self.industry_preference_list_view.as_view(), name='industry-list'),
            url(r'^industry_preference/create/$', self.industry_preference_create_view.as_view(),
                name='industry-create'),
            url(r'^industry_preference/(?P<pk>\d+)/$', self.industry_preference_manage_view.as_view(),
                name='industry-manage'),
            url(r'^industry_preference/(?P<pk>\d+)/delete/$', self.industry_preference_delete_view.as_view(),
                name='industry-delete'),



        ]
        return self.post_process_urls(urls)
application = PartnersDashboardApplication()
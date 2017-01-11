from oscar.apps.dashboard.partners.app import PartnersDashboardApplication as CorePartnersDashboardApplication
from django.conf.urls import url
from oscar.core.loading import get_class


class PartnersDashboardApplication(CorePartnersDashboardApplication):

    partner_address_manage_view = get_class('oscarapps.dashboard.partners.views', 'PartnerAddressManageView')

    store_type_list_view = get_class('oscarapps.dashboard.partners.views',
                                 'StoreTypeListView')

    store_type_create_view = get_class('oscarapps.dashboard.partners.views',
                                 'StoreTypeCreateView')
    store_type_manage_view = get_class('oscarapps.dashboard.partners.views',
                                 'StoreTypeManageView')
    store_type_delete_view = get_class('oscarapps.dashboard.partners.views',
                                 'StoreTypeDeleteView')


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



            url(r'^store_type/$', self.store_type_list_view.as_view(), name='store-type-list'),
            url(r'^store_type/create/$', self.store_type_create_view.as_view(),
                name='store-type-create'),
            url(r'^store_type/(?P<pk>\d+)/$', self.store_type_manage_view.as_view(),
                name='store-type-manage'),
            url(r'^store_type/(?P<pk>\d+)/delete/$', self.store_type_delete_view.as_view(),
                name='store-type-delete'),


        ]
        return self.post_process_urls(urls)
application = PartnersDashboardApplication()
from oscar.apps.dashboard.partners.app import PartnersDashboardApplication as CorePartnersDashboardApplication
from django.conf.urls import url
from oscar.core.loading import get_class


class PartnersDashboardApplication(CorePartnersDashboardApplication):

    partner_address_manage_view = get_class('oscarapps.dashboard.partners.views', 'PartnerAddressManageView')
    partner_filter_view = get_class('oscarapps.dashboard.partners.views', 'PartnerFilterView')


    store_type_list_view = get_class('oscarapps.dashboard.partners.views',
                                 'StoreTypeListView')

    store_type_create_view = get_class('oscarapps.dashboard.partners.views',
                                 'StoreTypeCreateView')
    store_type_manage_view = get_class('oscarapps.dashboard.partners.views',
                                 'StoreTypeManageView')
    store_type_delete_view = get_class('oscarapps.dashboard.partners.views',
                                 'StoreTypeDeleteView')



    brand_category_list_view = get_class('oscarapps.dashboard.partners.views',
                                 'BrandCategoryListView')
    brand_category_create_view = get_class('oscarapps.dashboard.partners.views',
                                 'BrandCategoryCreateView')
    brand_category_manage_view = get_class('oscarapps.dashboard.partners.views',
                                 'BrandCategoryManageView')
    brand_category_delete_view = get_class('oscarapps.dashboard.partners.views',
                                 'BrandCategoryDeleteView')

    brand_style_list_view = get_class('oscarapps.dashboard.partners.views',
                                 'BrandStyleListView')
    brand_style_create_view = get_class('oscarapps.dashboard.partners.views',
                                 'BrandStyleCreateView')
    brand_style_manage_view = get_class('oscarapps.dashboard.partners.views',
                                 'BrandStyleManageView')
    brand_style_delete_view = get_class('oscarapps.dashboard.partners.views',
                                 'BrandStyleDeleteView')


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



            url(r'^brand_category/$', self.brand_category_list_view.as_view(), name='brand-category-list'),
            url(r'^brand_category/create/$', self.brand_category_create_view.as_view(),
                name='brand-category-create'),
            url(r'^brand_category/(?P<pk>\d+)/$', self.brand_category_manage_view.as_view(),
                name='brand-category-manage'),
            url(r'^brand_category/(?P<pk>\d+)/delete/$', self.brand_category_delete_view.as_view(),
                name='brand-category-delete'),


            url(r'^brand_style/$', self.brand_style_list_view.as_view(), name='brand-style-list'),
            url(r'^brand_style/create/$', self.brand_style_create_view.as_view(),
                name='brand-style-create'),
            url(r'^brand_style/(?P<pk>\d+)/$', self.brand_style_manage_view.as_view(),
                name='brand-style-manage'),
            url(r'^brand_style/(?P<pk>\d+)/delete/$', self.brand_style_delete_view.as_view(),
                name='brand-style-delete'),


            url(r'^filter/$', self.partner_filter_view.as_view(), name='partner-filter'),


        ]
        return self.post_process_urls(urls)
application = PartnersDashboardApplication()
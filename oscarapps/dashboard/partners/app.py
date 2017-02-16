from oscar.apps.dashboard.partners.app import PartnersDashboardApplication as CorePartnersDashboardApplication
from django.conf.urls import url
from oscar.core.loading import get_class


class PartnersDashboardApplication(CorePartnersDashboardApplication):

    partner_address_manage_view = get_class('oscarapps.dashboard.partners.views', 'PartnerRentalInfoManageView')
    partner_filter_view = get_class('oscarapps.dashboard.partners.views', 'PartnerFilterView')

    sub_category_list_view = get_class('oscarapps.dashboard.partners.views',
                                 'BrandSubCategoryListView')

    sub_category_create_view = get_class('oscarapps.dashboard.partners.views',
                                 'BrandSubCategoryCreateView')
    sub_category_manage_view = get_class('oscarapps.dashboard.partners.views',
                                 'BrandSubCategoryManageView')
    sub_category_delete_view = get_class('oscarapps.dashboard.partners.views',
                                 'BrandSubCategoryDeleteView')

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
            url(r'^filter/$', self.partner_filter_view.as_view(), name='partner-filter'),

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

            url(r'^specialization/$', self.sub_category_list_view.as_view(), name='brand-sub-category-list'),
            url(r'^specialization/create/$', self.sub_category_create_view.as_view(),
                name='brand-sub-category-create'),
            url(r'^specialization/(?P<pk>\d+)/$', self.sub_category_manage_view.as_view(),
                name='brand-sub-category-manage'),
            url(r'^specialization/(?P<pk>\d+)/delete/$', self.sub_category_delete_view.as_view(),
                name='brand-sub-category-delete'),

            url(r'^store_type/$', self.brand_category_list_view.as_view(), name='brand-category-list'),
            url(r'^store_type/create/$', self.brand_category_create_view.as_view(),
                name='brand-category-create'),
            url(r'^store_type/(?P<pk>\d+)/$', self.brand_category_manage_view.as_view(),
                name='brand-category-manage'),
            url(r'^store_type/(?P<pk>\d+)/delete/$', self.brand_category_delete_view.as_view(),
                name='brand-category-delete'),

            url(r'^brand_style/$', self.brand_style_list_view.as_view(), name='brand-style-list'),
            url(r'^brand_style/create/$', self.brand_style_create_view.as_view(),
                name='brand-style-create'),
            url(r'^brand_style/(?P<pk>\d+)/$', self.brand_style_manage_view.as_view(),
                name='brand-style-manage'),
            url(r'^brand_style/(?P<pk>\d+)/delete/$', self.brand_style_delete_view.as_view(),
                name='brand-style-delete'),
        ]
        return self.post_process_urls(urls)
application = PartnersDashboardApplication()
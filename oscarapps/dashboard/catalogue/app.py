from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class


class CatalogueApplication(DashboardApplication):
    name = None

    default_permissions = ['is_staff', ]
    permissions_map = _map = {
        'catalogue-product': (['is_staff'], ['partner.dashboard_access']),
        'catalogue-product-create': (['is_staff'], ['partner.dashboard_access']),
        'catalogue-product-list': (['is_staff'], ['partner.dashboard_access']),

        'catalogue-product-delete': (['is_staff'], ['partner.dashboard_access']),
        'catalogue-product-lookup': (['is_staff'], ['partner.dashboard_access']),
        'catalogue-product-create-child': (['is_staff'], ['partner.dashboard_access']),
        'stock_alert_view': (['is_staff'], ['partner.dashboard_access']),
        'reserved-products': (['is_staff'], ['partner.dashboard_access']),

    }

    product_list_view = get_class('dashboard.catalogue.views',
                                  'ProductListView')
    product_lookup_view = get_class('dashboard.catalogue.views',
                                    'ProductLookupView')
    product_create_redirect_view = get_class('dashboard.catalogue.views',
                                             'ProductCreateRedirectView')
    product_createupdate_view = get_class('dashboard.catalogue.views',
                                          'ProductCreateUpdateView')
    product_delete_view = get_class('dashboard.catalogue.views',
                                    'ProductDeleteView')

    reserved_products_view = get_class('dashboard.catalogue.views',
                                 'ReservedProductsView')

    product_class_create_view = get_class('dashboard.catalogue.views',
                                          'ProductClassCreateView')
    product_class_update_view = get_class('dashboard.catalogue.views',
                                          'ProductClassUpdateView')
    product_class_list_view = get_class('dashboard.catalogue.views',
                                        'ProductClassListView')
    product_class_delete_view = get_class('dashboard.catalogue.views',
                                          'ProductClassDeleteView')

    category_list_view = get_class('dashboard.catalogue.views',
                                   'CategoryListView')
    category_detail_list_view = get_class('dashboard.catalogue.views',
                                          'CategoryDetailListView')
    category_create_view = get_class('dashboard.catalogue.views',
                                     'CategoryCreateView')
    category_update_view = get_class('dashboard.catalogue.views',
                                     'CategoryUpdateView')
    category_delete_view = get_class('dashboard.catalogue.views',
                                     'CategoryDeleteView')

    stock_alert_view = get_class('dashboard.catalogue.views',
                                 'StockAlertListView')
    attribute_list_view = get_class('dashboard.catalogue.views',
                                    'AttributeListView')
    attribute_manage_view = get_class('dashboard.catalogue.views',
                                      'AttributeManageView')
    attributeoptionscreateview = get_class('dashboard.catalogue.views',
                                           'AttributeOptionsCreateView')
    attributeoptionsdeleteview = get_class('dashboard.catalogue.views',
                                           'AttributeOptionsDeleteView')
    optionslistview = get_class('dashboard.catalogue.views',
                                'OptionsListView')
    optionmanageview = get_class('dashboard.catalogue.views',
                                 'OptionManageView')
    Options_create_View = get_class('dashboard.catalogue.views',
                                    'OptionsCreateView')
    Options_Delete_View = get_class('dashboard.catalogue.views',
                                    'OptionsDeleteView')

    def get_urls(self):
        urls = [
            url(r'^products/(?P<pk>\d+)/$',
                self.product_createupdate_view.as_view(),
                name='catalogue-product'),
            url(r'^products/create/$',
                self.product_create_redirect_view.as_view(),
                name='catalogue-product-create'),
            url(r'^products/create/(?P<product_class_slug>[\w-]+)/$',
                self.product_createupdate_view.as_view(),
                name='catalogue-product-create'),
            url(r'^products/(?P<parent_pk>[-\d]+)/create-variant/$',
                self.product_createupdate_view.as_view(),
                name='catalogue-product-create-child'),
            url(r'^products/(?P<pk>\d+)/delete/$',
                self.product_delete_view.as_view(),
                name='catalogue-product-delete'),
            url(r'^$', self.product_list_view.as_view(),
                name='catalogue-product-list'),
            url(r'^stock-alerts/$', self.stock_alert_view.as_view(),
                name='stock-alert-list'),
            url(r'^product-lookup/$', self.product_lookup_view.as_view(),
                name='catalogue-product-lookup'),
            url(r'^categories/$', self.category_list_view.as_view(),
                name='catalogue-category-list'),
            url(r'^categories/(?P<pk>\d+)/$',
                self.category_detail_list_view.as_view(),
                name='catalogue-category-detail-list'),
            url(r'^categories/create/$', self.category_create_view.as_view(),
                name='catalogue-category-create'),
            url(r'^categories/create/(?P<parent>\d+)$',
                self.category_create_view.as_view(),
                name='catalogue-category-create-child'),
            url(r'^categories/(?P<pk>\d+)/update/$',
                self.category_update_view.as_view(),
                name='catalogue-category-update'),
            url(r'^categories/(?P<pk>\d+)/delete/$',
                self.category_delete_view.as_view(),
                name='catalogue-category-delete'),
            url(r'^product-type/create/$',
                self.product_class_create_view.as_view(),
                name='catalogue-class-create'),
            url(r'^product-types/$',
                self.product_class_list_view.as_view(),
                name='catalogue-class-list'),
            url(r'^product-type/(?P<pk>\d+)/update/$',
                self.product_class_update_view.as_view(),
                name='catalogue-class-update'),
            url(r'^product-type/(?P<pk>\d+)/delete/$',
                self.product_class_delete_view.as_view(),
                name='catalogue-class-delete'),
            url(r'^attributes/$', self.attribute_list_view.as_view(),
                name='attribute-options'),
            url(r'^attributes/(?P<pk>\d+)/$', self.attribute_manage_view.as_view(),
                name='attribute-options-manage'),
            url(r'^attributes/create/$', self.attributeoptionscreateview.as_view(),
                name='attribute-options-create'),
            url(r'^attributes/(?P<pk>\d+)/delete/$', self.attributeoptionsdeleteview.as_view(),
                name='attribute-options-delete'),
            url(r'^attributes_options/$', self.optionslistview.as_view(),
                name='size-options-list'),
            url(r'^attributes_options/(?P<pk>\d+)$', self.optionmanageview.as_view(),
                name='size-options-manage'),
            url(r'^attributes_options/create/$', self.Options_create_View.as_view(),
                name='size-options-create'),
            url(r'^attributes_optoins/(?P<pk>\d+)/delete/$', self.Options_Delete_View.as_view(),
                name='size-options-delete'),
            url(r'^reserved-products/$',
                self.reserved_products_view.as_view(),
                name='reserved-products'),

        ]
        return self.post_process_urls(urls)


application = CatalogueApplication()

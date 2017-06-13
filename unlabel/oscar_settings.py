from django.utils.translation import ugettext_lazy as _

from oscar.defaults import *


OSCAR_SHOP_NAME = 'Unlabel'
AUTH_USER_MODEL = "users.User"

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
PASSWORD_RESET_TIMEOUT_DAYS = 1

OSCAR_DEFAULT_CURRENCY = 'USD'
OSCAR_DASHBOARD_NAVIGATION = [
    {
        'label': _('Dashboard'),
        'icon': 'icon-th-list',
        'url_name': 'dashboard:index',
    },
    # {
    #     'label': _('Catalogue'),
    #     'icon': 'icon-sitemap',
    #     'children': [
    #         {
    #             'label': _('Products'),
    #             'url_name': 'dashboard:catalogue-product-list',
    #         },
    #         {
    #             'label': _('Departments'),
    #             'url_name': 'dashboard:catalogue-class-list',
    #         },
    #         {
    #             'label': _('Categories'),
    #             'url_name': 'dashboard:catalogue-category-list',
    #         },
    #         {
    #             'label': _('Ranges'),
    #             'url_name': 'dashboard:range-list',
    #         },
    #         {
    #             'label': _('Low stock alerts'),
    #             'url_name': 'dashboard:stock-alert-list',
    #         },
    #         {
    #             'label': _('Promoted Items'),
    #             'url_name': 'dashboard:Promoted-Products',
    #         },
    #         {
    #             'label': _('Excluded From Search'),
    #             'url_name': 'dashboard:search-excluded-products',
    #         },
    #     ]
    # },
    {
        'label': _('Inventory Management'),
        'icon': 'icon-sitemap',
        'children': [
            {
                'label': _('Products'),
                'url_name': 'dashboard:catalogue-product-list',
            },
            {
                'label': _('Reserved Products'),
                'url_name': 'dashboard:reserved-products',
            },
            {
                'label': _('Departments'),
                'url_name': 'dashboard:catalogue-class-list',
            },

            {
                'label': _('Categories'),
                'url_name': 'dashboard:catalogue-category-list',
            },
            {
                'label': _('Ranges'),
                'url_name': 'dashboard:range-list',
            },
            {
                'label': _('Low stock alerts'),
                'url_name': 'dashboard:stock-alert-list',
            },

        ]
    },
    {
        'label': _('Fulfilment'),
        'icon': 'icon-shopping-cart',
        'children': [
            {
                'label': _('Orders'),
                'url_name': 'dashboard:order-list',
            },
            {
                'label': _('Statistics'),
                'url_name': 'dashboard:order-stats',
            },
            # The shipping method dashboard is disabled by default as it might
            # be confusing. Weight-based shipping methods aren't hooked into
            # the shipping repository by default (as it would make
            # customising the repository slightly more difficult).
            {
                'label': _('Shipping charges'),
                'url_name': 'dashboard:shipping-method-list',
            },
        ]
    },
    {
        'label': _('Partners'),
        'icon': 'icon-user',
        'children': [
            {
                'label': _('Brands'),
                'url_name': 'dashboard:partner-list',
            },
            {
                'label': _('Influencers'),
                'url_name': 'dashboard:influencer-list',
            },
        ]
    },

    {
        'label': _('Users'),
        'icon': 'icon-group',
        'url_name': 'dashboard:users-index',
        # 'children': [
        #     {
        #         'label': _('Users'),
        #         'url_name': 'dashboard:users-index',
        #     },
        #     {
        #         'label': _('Stock alert requests'),
        #         'url_name': 'dashboard:user-alert-list',
        #     },
        # ]
    },
    {
        'label': _('Offers'),
        'icon': 'icon-bullhorn',
        'children': [
            {
                'label': _('Offers'),
                'url_name': 'dashboard:offer-list',
            },
            {
                'label': _('Vouchers'),
                'url_name': 'dashboard:voucher-list',
            },
        ],
    },
    {
        'label': _('Content'),
        'icon': 'icon-folder-close',
        'children': [
            {
                'label': _('Content blocks'),
                'url_name': 'dashboard:promotion-list',
            },
            {
                'label': _('Content blocks by page'),
                'url_name': 'dashboard:promotion-list-by-page',
            },
            {
                'label': _('Pages'),
                'url_name': 'dashboard:page-list',
            },
            {
                'label': _('Email templates'),
                'url_name': 'dashboard:comms-list',
            },
            {
                'label': _('Reviews'),
                'url_name': 'dashboard:reviews-list',
            },
        ]
    },
    {
        'label': _('Reports'),
        'icon': 'icon-bar-chart',
        'url_name': 'dashboard:reports-index',
    },
    {
        'label': _('CRUD'),
        'icon': 'icon-edit',
        'children': [
            # {
            #     'label': _('Style Preferences'),
            #     'url_name': 'dashboard:style-list',
            # },
            {
                'label': _('Brand Styles'),
                'url_name': 'dashboard:brand-style-list',
            },

            {
                'label': _('Store Type'),
                'url_name': 'dashboard:brand-category-list',
            },
            {
                'label': _('Brand Specialization'),
                'url_name': 'dashboard:brand-sub-category-list',
            },
            {

                'label': _('Locations'),
                'url_name': 'dashboard:location-list',
            },
            {
                'label': _('Size Classes'),
                'url_name': 'dashboard:attribute-options',
            },
            {
                'label': _('Size Options'),
                'url_name': 'dashboard:size-options-list',
            },
        ],
    },
    {
        'label': _('Payment'),
        'icon': 'icon-money',
        'children': [
            {
                'label': _('Payout Now'),
                'url_name': 'dashboard:payout',
            },
        ]
    },

]
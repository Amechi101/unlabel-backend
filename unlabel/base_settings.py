"""
Django settings for unlabel project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
from django.utils.translation import ugettext_lazy as _
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import json
import dj_database_url
from oscar.defaults import *
OSCAR_DASHBOARD_NAVIGATION = [
    {
        'label': _('Dashboard'),
        'icon': 'icon-th-list',
        'url_name': 'dashboard:index',
    },
    {
        'label': _('Catalogue'),
        'icon': 'icon-sitemap',
        'children': [
            {
                'label': _('Products'),
                'url_name': 'dashboard:catalogue-product-list',
            },
            {
                'label': _('Product Types'),
                'url_name': 'dashboard:catalogue-class-list',
            },
            {
                'label': _('Style Preferences'),
                'url_name': 'dashboard:style-list',
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
            {
                'label': _('Brands'),
                'url_name': 'dashboard:partner-list',
            },
            {
                'label': _('Influencers'),
                'url_name': 'dashboard:influencer-list',
            },

            # The shipping method dashboard is disabled by default as it might
            # be confusing. Weight-based shipping methods aren't hooked into
            # the shipping repository by default (as it would make
            # customising the repository slightly more difficult).
            # {
            #     'label': _('Shipping charges'),
            #     'url_name': 'dashboard:shipping-method-list',
            # },
        ]
    },
    {
        'label': _('Customers'),
        'icon': 'icon-group',
        'children': [
            {
                'label': _('Customers'),
                'url_name': 'dashboard:users-index',
            },
            {
                'label': _('Stock alert requests'),
                'url_name': 'dashboard:user-alert-list',
            },
        ]
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
]
# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, "fixtures", "secrets.json")) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """
    Get the secret variable or return explicit exception.
    """

    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


cloudinary.config(
    cloud_name=get_secret("CLOUDINARY_CLOUD_NAME"),
    api_key=get_secret("CLOUDINARY_API_KEY"),
    api_secret=get_secret("CLOUDINARY_API_SECRET")
)

SECRET_KEY = get_secret("SECRET_KEY")


# Application definition
INSTALLED_APPS = [
    # external
    'material',
    'material.admin',

    # django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',

    # external
    'cloudinary',
    'bootstrap3',
    'tastypie',
    'widget_tweaks',


    # project
    'unlabel',
    'unlabel_api',
    'applications',
    'oscarapps.influencers',

    #oscar-api
    'rest_framework',
    'oscarapi',
    'rest_framework.authtoken',
    'rest_auth',
]

from oscar import get_core_apps

INSTALLED_APPS = INSTALLED_APPS + get_core_apps(
    [
        'oscarapps.partner',
        'oscarapps.customer',
        'oscarapps.catalogue',
        'oscarapps.address',
        'oscarapps.dashboard',
        'oscarapps.dashboard.partners',
        'oscarapps.dashboard.catalogue'
    ])

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'oscar.apps.basket.middleware.BasketMiddleware',

    # api and oscar view mix middleware
    'oscarapi.middleware.ApiBasketMiddleWare',
    # session management
    'oscarapi.middleware.HeaderSessionMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

ROOT_URLCONF = 'unlabel.urls'

# TEMPLATES = [
# {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': ['unlabel/templates', 'applications/templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.contrib.auth.context_processors.auth',
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.i18n',
#                 'django.template.context_processors.media',
#                 'django.template.context_processors.static',
#                 'django.template.context_processors.tz',
#                 'django.template.context_processors.request',
#                 'django.contrib.messages.context_processors.messages',
#                 'unlabel.context_processors.theme',
#                 'unlabel.context_processors.consts',
#             ]
#         },
#     },
# ]
from oscar import OSCAR_MAIN_TEMPLATE_DIR

TEMPLATES = [
   {
       'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'DIRS': [
                   os.path.join(BASE_DIR, 'oscarapps/templates'),
                   OSCAR_MAIN_TEMPLATE_DIR
               ] + ['unlabel/templates', 'applications/templates'],
       'APP_DIRS': True,
       'OPTIONS': {
           'context_processors': [
               'django.template.context_processors.debug',
               'django.template.context_processors.request',
               'django.contrib.auth.context_processors.auth',
               'django.contrib.messages.context_processors.messages',
               'django.template.context_processors.i18n',
               'django.template.context_processors.media',
               'django.template.context_processors.tz',

               'oscar.apps.search.context_processors.search_form',
               'oscar.apps.promotions.context_processors.promotions',
               'oscar.apps.checkout.context_processors.checkout',
               'oscar.apps.customer.notifications.context_processors.notifications',
               'oscar.core.context_processors.metadata',

               'unlabel.context_processors.theme',
               'unlabel.context_processors.consts',
           ],
       },
   },
]

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

WSGI_APPLICATION = 'unlabel.wsgi.application'

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, "fixtures"),
]


# Administration
LOGIN_URL = '/admin/login/'
LOGOUT_URL = '/admin/logout/'
LOGIN_REDIRECT_URL = '/admin/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "unlabel", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Api settings
TASTYPIE_DEFAULT_FORMATS = ['json']

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
SITE_ID = int(os.environ.get("SITE_ID", 1))

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# REST_FRAMEWORK = {
#     'PAGINATE_BY': 1,
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'MAX_PAGINATE_BY': 100,
#     'DEFAULT_PERMISSION_CLASSES': (
#         # 'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.BasicAuthentication',
#     ),
#     # 'DEFAULT_RENDERER_CLASSES': (
#     #     'rest_framework.renderers.JSONRenderer',
#     # ),
#     'DEFAULT_PARSER_CLASSES': (
#         'rest_framework.parsers.JSONParser',
#     )
# }


#---Site Email Settings----

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'unlabelapp123'
EMAIL_HOST_USER = 'unlabelapp@gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'unlabelapp@gmail.com'

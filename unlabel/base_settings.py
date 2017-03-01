"""
Django settings for unlabel project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import json

from django.core.exceptions import ImproperlyConfigured

from oscar import get_core_apps
from oscar import OSCAR_MAIN_TEMPLATE_DIR

from unlabel.oscar_settings import *

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOSITORY_ROOT = os.path.dirname(BASE_DIR)

with open(os.path.join(BASE_DIR, "fixtures", "secrets.json")) as f:
    secrets = json.loads(f.read())


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_SECURE_URLS = False       # use http instead of https
AWS_QUERYSTRING_AUTH = False     # don't add complex authentication-related query parameters for requests
AWS_S3_ACCESS_KEY_ID = 'AKIAIWCAMKSI7I763E7A'     # enter your access key id
AWS_S3_SECRET_ACCESS_KEY = 'XaCKTRxXb/NBS60sQhJAvnWh6NcKpQJjlg80K0xb' # enter your secret access key
AWS_STORAGE_BUCKET_NAME = 'unlabel'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN
MEDIA_ROOT = '%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
OSCAR_MISSING_IMAGE_URL = MEDIA_URL + 'image_not_found.jpg'


AWS_ACCESS_KEY = 'AKIAIWCAMKSI7I763E7A'
AWS_SECRET_ACCESS_KEY = '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'
SCARFACE_REGION_NAME = 'ap-south-1'
SCARFACE_LOGGING_ENABLED = True

STRIPE_API_KEY = "sk_test_STJxYzsopQx9fd4xIcE4EzT9"
STRIPE_CLIENT_ID = "ca_AB3gizjA9Uhs9g2AsaOWzBiII3LxRLl6"

SCARFACE_APNS_CERTIFICATE = "-----BEGIN CERTIFICATE-----\nMIIFlzCCBH+gAwIBAgIIFy2yaV/8fd8wDQYJKoZIhvcNAQEFB\
QAwgZYxCzAJBgNV\nBAYTAlVTMRMwEQYDVQQKDApBcHBsZSBJbmMuMSwwKgYDVQQLDCNBcHBsZSBXb3Js\nZHdpZGUgRGV2ZWxvcGVy\
IFJlbGF0aW9uczFEMEIGA1UEAww7QXBwbGUgV29ybGR3\naWRlIERldmVsb3BlciBSZWxhdGlvbnMgQ2VydGlmaWNhdGlvbiBBdXRob3Jpd\
Hkw\nHhcNMTcwMjAyMDUzNjI0WhcNMTgwMjAyMDUzNjI0WjCBljEpMCcGCgmSJomT8ixk\nAQEMGWNvbS51bmxhYmVsLmluZmx1ZW5jZXJBc\
HAxRzBFBgNVBAMMPkFwcGxlIERl\ndmVsb3BtZW50IElPUyBQdXNoIFNlcnZpY2VzOiBjb20udW5sYWJlbC5pbmZsdWVu\nY2VyQXBwMRMwEQ\
YDVQQLDAo4WVQ1VkxKUktIMQswCQYDVQQGEwJVUzCCASIwDQYJ\nKoZIhvcNAQEBBQADggEPADCCAQoCggEBAL8jWApYPk1NOUuO8VKs38mDm\
N4SS7Bm\nWYC1B945N72i0SBRt1BDUfCLnDMlro8QrQEzoDUe1UMyAf0bN0728/eIrvIQ/Ex9\nchNX8c4q9F1LxlU4aGlwTvikTBYQ5BR40AY\
ZC5Lc84pXWoAD92kDYvb32/X1kFgk\nVifqxBcQr3/utoBccluRQW8//fm0BCXbtBsAQyjmbAxPBk2fxpNIp6M2nIVy62fm\nIt5DfpbqMCBvdB\
m4lTabZP5rX5oINk/kOkiwa0z7oHpwjw9n3TiaenzJbDeNFFGp\nxFmNu1PRj5MVlxKYe+swIH2zgnr5MAcmb1+BRA5aGp1kuLyJHCkxGDsCAw\
EAAaOC\nAeUwggHhMB0GA1UdDgQWBBTc6jAsVD0W3oqmZkhadRwVeaeQtDAJBgNVHRMEAjAA\nMB8GA1UdIwQYMBaAFIgnFwmpthhgi+zruvZH\
WcVSVKO3MIIBDwYDVR0gBIIBBjCC\nAQIwgf8GCSqGSIb3Y2QFATCB8TCBwwYIKwYBBQUHAgIwgbYMgbNSZWxpYW5jZSBv\nbiB0aGlzIGNlcnR\
pZmljYXRlIGJ5IGFueSBwYXJ0eSBhc3N1bWVzIGFjY2VwdGFu\nY2Ugb2YgdGhlIHRoZW4gYXBwbGljYWJsZSBzdGFuZGFyZCB0ZXJtcyBhbmQg\
Y29u\nZGl0aW9ucyBvZiB1c2UsIGNlcnRpZmljYXRlIHBvbGljeSBhbmQgY2VydGlmaWNh\ndGlvbiBwcmFjdGljZSBzdGF0ZW1lbnRzLjApBgg\
rBgEFBQcCARYdaHR0cDovL3d3\ndy5hcHBsZS5jb20vYXBwbGVjYS8wTQYDVR0fBEYwRDBCoECgPoY8aHR0cDovL2Rl\ndmVsb3Blci5hcHBsZS5\
jb20vY2VydGlmaWNhdGlvbmF1dGhvcml0eS93d2RyY2Eu\nY3JsMAsGA1UdDwQEAwIHgDATBgNVHSUEDDAKBggrBgEFBQcDAjAQBgoq\
hkiG92Nk\nBgMBBAIFADANBgkqhkiG9w0BAQUFAAOCAQEAa45OQDe3HhSlxTJXn1M80oPfTT+k\nMFD/JpojjZSTQTh0J0luWk308lr3ujS4nC\
TWuzSeMbr1no5qYfoE0OPe/7pmG0fK\n9H1sMEYd43kFKL2LhcgjvQx3dOhuyA+CD7Etxi0PD96tME4gumpFZ4WfHktv4tfK\nCvUDm9z1yh61G\
ZPelBDF++t7iP8xzWf6RW99H1dGeeinI68H2S5bkCWgBI4KVb3Y\ntciJiMjF0v1z1AOabqwwCw6iHzuQ4RyHk9Rf6JD8G3elt+exP2sRfCVagh\
0xI5PD\nE5dFJXPGWNaRaPeYdAB+EnAH5pf/ciFVqYVH8+VVQVhPI8zsMLrerq/veA==\n-----END CERTIFICATE-----"


SCARFACE_APNS_PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAo\
IBAQC/I1gKWD5NTTlL\njvFSrN/Jg5jeEkuwZlmAtQfeOTe9otEgUbdQQ1Hwi5wzJa6PEK0BM6A1HtVDMgH9\nGzdO9vP3iK7yEPxMfXIT\
V/HOKvRdS8ZVOGhpcE74pEwWEOQUeNAGGQuS3POKV1qA\nA/dpA2L299v19ZBYJFYn6sQXEK9/7raAXHJbkUFvP/35tAQl27QbAEMo5mwM\
TwZN\nn8aTSKejNpyFcutn5iLeQ36W6jAgb3QZuJU2m2T+a1+aCDZP5DpIsGtM+6B6cI8P\nZ904mnp8yWw3jRRRqcRZjbtT0Y+TFZcSmHvrMCB\
9s4J6+TAHJm9fgUQOWhqdZLi8\niRwpMRg7AgMBAAECggEAT6Y80+K945ygmZnxelBL2T+bfj8Fh3a/KWFG7BXP4phs\nqRkkWLAU/zZOWwoC2d9\
LGMsYoco9eIjoRz8GJ0PFmos8y+bEHGPSG7l0LEO+HPqs\npWqiJ/4DCp38jt1vDhDiLwhUyFiGrEmGjv4YJYyhuuTCppY0Fmb\
d+DheinYLjDWH\nO6h4f9yDEpuU2A9UefwzTheYQGWoee9XletLAIzOOt+kNB/eGGMGLxWjJ1dCxvGL\n3KVUwytwjwwRkBUqlcqp6\
pErpKXg5UNjs0HrhEqL8wHErtqhYvfGLWrwI+DjrTJ0\nMD4o6sS5BwgSNQY8UMrR43HLgU1IxB/sF1LKGdQMoQKBgQDgGe73PG\
FULbEtZK7T\nIc4/Y5dfvavE2jkzuqL/WvK8r+zVRIJ8NVNLiEGN1DsgsFy+BTCHKOtMNRkDQJmu\nJvM3YtwH9D4iNM/HKZYdG0cW\
p2xDQtJBs2Cmr0LF/k7BD5c1ncrcTcCLbseZ2UR2\nBMHBmEcyQShmnxynX5U8YWc5MwKBgQDaWEHVtSjQCWIzSsvkuB\
Sa/xx8+z/4IiH0\n8hYZBI5ltp8uzKpMD9xwd1yG9T4V4pTBruheEGK6QYHmMykthkZMIi/kyFTBCma/\nZiHaJzSHa7kjoDPp\
dO+fUC5MFz17WRXK/9U+MXPSNzM2oXB47SkEaK9iQaXFAMS8\n8wBFkx/02QKBgQDQ4ntiyk4yZ5CxrhpixCz52vu7CxFzoLEW7Y2HFa\
ASjqzjsUMr\nQY1NZ0krSTp/4sPffvjX0yVX2FpjNLDKqpWj96r+YwQTYESX8MRyhv2BOTdpjnxr\nLycU12IXKU8BF2YrXNQ8+uBRV0Y\
HuoPcudxcdnNOfXuKBB9yR17UdDoCDwKBgGzy\njt8Qxu2PURWg474bcASq+M8QGyo39dOgHBCdqmPsTN9wNiU/4NGpbV\
zV8AXBilJe\ncQnGiUzAtQ1lR820a00/3b/9ifTMuNoWHxwYZeiQgs/Y9y4tMAfBXWiQTBhJKkuh\nfgjLaixhaMeApHticw4FIk\
YX1ZxINuLFKcSNlet5AoGBAJzPYZU0e92ShlD/1qFC\nfJbv2VmBApIER/iZRg8CL0U48OY8hV1Li9cuXv/rA6ZZ6vhK08hVaVNbBTg\
LYEoL\n0fwTtvsrUVHcSGtFna7AtJrisWWev2kTLNGLioXNPEOczDEzniJlwoG2NNTRIyJK\nvNYc1hkssQE9PLLGolkHf6kA\n-----END PRIVATE KEY-----"

def get_secret(setting, secrets=secrets):
    """
    Get the secret variable or return explicit exception.
    """

    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")

# Application definition
INSTALLED_APPS = [
    # external
    'scarface',
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
    'storages',
    'multiselectfield',

    # project
    'unlabel',
    'unlabel_api',
    'applications',
    'oscarapps.influencers',

    #oscar-api
    'oscarapi',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',

    'allauth',
    'allauth.account',
    'rest_auth.registration',

    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    ###for oscar-api over ride
    'api_v2',

    ### for user
    'users',
]

INSTALLED_APPS = INSTALLED_APPS + get_core_apps(
    [
        'oscarapps.customer',
        'oscarapps.partner',
        'oscarapps.payment',
        'oscarapps.catalogue',
        'oscarapps.address',
        'oscarapps.dashboard',
        'oscarapps.dashboard.partners',
        'oscarapps.dashboard.catalogue',
        'oscarapps.dashboard.users',
        'oscarapps.checkout',
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
    'allauth.account.auth_backends.AuthenticationBackend',
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

               'django.core.context_processors.request',
               'django.contrib.auth.context_processors.auth',
               # 'allauth.account.context_processors.account',
               # 'allauth.socialaccount.context_processors.socialaccount',
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
# LOGIN_URL = '/admin/login/'
# LOGOUT_URL = '/admin/logout/'
# LOGIN_REDIRECT_URL = '/admin/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "unlabel", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),
                   ]
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


REST_FRAMEWORK = {
    # 'PAGINATE_BY': 1,
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'MAX_PAGINATE_BY': 100,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 6,
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 'DEFAULT_PARSER_CLASSES': (
    #     'rest_framework.parsers.JSONParser',
    # )
}


#---Site Email Settings----

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'unlabelapp123'
EMAIL_HOST_USER = 'unlabelapp@gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'unlabelapp@gmail.com'

assert len(SECRET_KEY) > 20, 'Please set SECRET_KEY in local_settings.py'

SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'}}

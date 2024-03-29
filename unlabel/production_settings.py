from unlabel.base_settings import *

# DEBUG = False
DEBUG = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')

# SECURE_SSL_REDIRECT = True
SECURE_SSL_REDIRECT = False

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

# SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = False

# CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = False

# CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False

X_FRAME_OPTIONS = 'DENY'

# DATABASES = {
#     'default': dj_database_url.config(default=get_secret("BRANDS_PRODUCTION_DB_URL")),
# }

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'unlabel_dev',
       'USER': 'prod',
       'PASSWORD': 'prod',
       'HOST': '127.0.0.1',
       'PORT': '5432',
   }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60
    }
}



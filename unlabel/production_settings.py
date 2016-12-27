from unlabel.base_settings import *

DEBUG = False

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True  

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

CSRF_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = 'DENY'

DATABASES = {
    'default': dj_database_url.config(default=get_secret("BRANDS_PRODUCTION_DB_URL")),
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'TIMEOUT': 60
    }
}

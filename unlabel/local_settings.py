from unlabel.base_settings import *

DEBUG = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')

DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': 'unlabel_db',
      'USER': 'unlabel_user',
      'PASSWORD': 'unlabel_pass',
      'HOST': '127.0.0.1',
      'PORT': '5432',
  }
}

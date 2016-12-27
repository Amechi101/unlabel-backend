from django.conf import settings

from appconf import AppConf

class ThemeAppConf(AppConf):
    
    VERSION = 7.0
    PRODUCTION_URL = "https://unlabel.us"
    CONTACT_EMAIL = "info@unlabel.us"
    
    class Meta:
        prefix = "theme"

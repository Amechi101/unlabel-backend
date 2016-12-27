import cloudinary

from django.contrib.sites.models import Site

from unlabel.conf import settings

def consts(request):
    return dict(
        BRANDIMAGES = {
        	"format": "jpg",
            "crop": "fill",
            "height":900,
            "width":900,
            "fetch_format":"auto",
            "quality":"auto"
        }
    )

def theme(request):
    ctx = {
        "THEME_VERSION":settings.THEME_VERSION,
        "THEME_PRODUCTION_URL":settings.THEME_PRODUCTION_URL,
        "THEME_CONTACT_EMAIL": settings.THEME_CONTACT_EMAIL
    }
    
    if Site._meta.installed:
        site = Site.objects.get_current()
        ctx.update({
            "SITE_NAME": site.name,
            "SITE_DOMAIN": site.domain
        })
    
    return ctx

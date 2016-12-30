from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url, patterns
from django.conf import settings
from django.views.generic import TemplateView

from unlabel.views import HomePageView, LegalStuffView, PrivacyPolicyView, ContactView, AboutView
from applications.views import BrandInviteView
from oscar.app import application
from django.conf.urls.i18n import i18n_patterns

from oscarapi.app import application as api

urlpatterns = [
	# admin
	url(r"^admin/", include(admin.site.urls)),
	# url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
	# url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
	# url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
	# url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
	
	# site
    url(r'^$', HomePageView.as_view(), name="home" ),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r"^oscar/", include(application.urls)),
    url(r"^about/$", AboutView.as_view(), name="about"),
    url(r"^terms/$", LegalStuffView.as_view(), name="terms"),
    url(r"^privacy-policy/$", PrivacyPolicyView.as_view(), name="privacy-policy"),
    url(r"^contact/$", ContactView.as_view(), name="contact"),
	url(r'^(?P<slug>[\w\d-]+)-invite/$', BrandInviteView.as_view(), name="brand_invite"),

   	# brands
	url(r"^brands/", include('applications.urls')),

    # influencers
	url(r"^unlabel-discovery/", include('oscarapps.influencers.urls')),

    # api's
	url(r"unlabel-network/", include('unlabel_api.urls')),

    # api_v2
    url(r'^api/', include(api.urls)),

    url(r'^api_v2/',include('api_v2.urls')),
]



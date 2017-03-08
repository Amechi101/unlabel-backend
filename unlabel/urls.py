from django.contrib import admin
from django.conf.urls import include, url
from oscarapi.app import application as api

from unlabel.views import HomePageView, LegalStuffView, PrivacyPolicyView, ContactView, AboutView
from applications.views import BrandInviteView
from oscar.app import application
from oscar.core.loading import get_class

# from api_v2.app import application as oscar_override_api

home_view = get_class('promotions.views', 'HomeView')
stripe_view = get_class('dashboard.views',
                                 'StripeView')

urlpatterns = [  # admin
                 url(r"^admin/", include(admin.site.urls)),
                 # url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
                 # url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
                 # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
                 # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),  # site
                 # url(r'^$', HomePageView.as_view(), name="home"),
                 url(r'^$', home_view.as_view(), name='home'),
                 url(r'^i18n/', include('django.conf.urls.i18n')),
                 url(r"^", include(application.urls)),
                 url(r"^about/$", AboutView.as_view(), name="about"),
                 url(r"^terms/$", LegalStuffView.as_view(), name="terms"),
                 url(r"^privacy-policy/$", PrivacyPolicyView.as_view(), name="privacy-policy"),
                 url(r"^contact/$", ContactView.as_view(), name="contact"),
                 url(r'^(?P<slug>[\w\d-]+)-invite/$', BrandInviteView.as_view(), name="brand_invite"),  # brands
                 url(r"^brands/", include('applications.urls')),

                 # influencers
                 url(r"^influencers/", include('oscarapps.influencers.urls')),

                 # partners
                 url(r"^partners/", include('oscarapps.partner.urls')),

                 # api's
                 url(r"unlabel-network/", include('unlabel_api.urls')),

                 # api_v2
                 url(r'^api/', include(api.urls)),

                 # url(r'oscar_override_api/',include(oscar_override_api.urls)),

                 url(r'^api_v2/', include('api_v2.urls')),

                 url(r'^rest-auth/', include('rest_auth.urls')),


                 # url(r'^pay/', include('oscarapps.checkout.urls')),

                url(r'^stripe',
                  stripe_view.as_view(),
                  name='stripe'),


                 ]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



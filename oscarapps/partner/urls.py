from django.conf.urls import url

from oscarapps.partner.views import PartnerSignUpView

urlpatterns = [
    url(r'partner-sign-up/(?P<code>[0-9A-Za-z_\-]+)/$',
        PartnerSignUpView.as_view(), name='partner-signup-view')
]



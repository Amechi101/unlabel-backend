from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from oscarapps.partner.views import PartnerSignUpView, BrandListView, BrandDetailView

urlpatterns = [
    url(r'partner-sign-up/(?P<code>[0-9A-Za-z_\-]+)/$',
        PartnerSignUpView.as_view(), name='partner-signup-view'),

    url(r'^brand/$', BrandListView.as_view(), name='brand-list'),
    url(r'^brand/(?P<slug>[\w-]+)/$', login_required(BrandDetailView.as_view()), name='brand_detail'),
]



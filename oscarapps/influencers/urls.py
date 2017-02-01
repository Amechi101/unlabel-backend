from django.conf.urls import url

from oscarapps.influencers.views import InfluencerListView, InfluencerDetailView, InfluencerSignUpView


urlpatterns = [
    url(r'unlabel-influencers/$', InfluencerListView.as_view(), name="influencers"),
    url(r'^unlabel-influencer/(?P<slug>[\w\d-]+)/$', InfluencerDetailView.as_view(), name="influencer_detail"),
    url(r'^influencer-sign-up/(?P<code>[0-9A-Za-z_\-]+)/$',
        InfluencerSignUpView.as_view(), name='influencer-signup-view')
]





from django.conf.urls import include, url

from influencers.views import InfluencerListView, InfluencerDetailView


urlpatterns = [
	url(r'unlabel-influencers/$', InfluencerListView.as_view(), name="influencers"),
	url(r'^unlabel-influencer/(?P<slug>[\w\d-]+)/$', InfluencerDetailView.as_view(), name="influencer_detail"),
]

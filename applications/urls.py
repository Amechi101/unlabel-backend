from django.conf.urls import include, url

from views import BrandDetailView


urlpatterns = [
	# brand detail
	url(r'^(?P<slug>[\w\d-]+)/$', BrandDetailView.as_view(), name="brand_detail"),
]


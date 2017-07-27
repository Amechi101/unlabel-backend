from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from oscar.apps.customer.app import CustomerApplication as CoreCustomerApplication
from oscar.core.application import Application
from oscar.core.loading import get_class
from oscarapps.customer.views import BrandView, BrandUnfollowView, InfluencerView, InfluencerUnfollowView
from oscarapps.customer.views import ProductsView, BankcardView, BankcardDeleteView, NotificationsSettingsView, \
    BrandFollowUnfollowView, UccFollowUnfollowView, ProductLikeUnlikeView


class CustomerApplication(CoreCustomerApplication):
    def get_urls(self):
        urls = super(CustomerApplication, self).get_urls()
        urls += [
            url(r'^followed-brands/$',
                login_required(BrandView.as_view()), name='followed-brands'),

            url(r'^unfollow-brand/(?P<pk>\d+)$',
                login_required(BrandUnfollowView.as_view()), name='unfollow-brand'),

            url(r'^follow-unfollow-brand/(?P<pk>\d+)$',
                login_required(BrandFollowUnfollowView.as_view()), name='follow-unfollow-brand'),

            url(r'^follow-unfollow-ucc/(?P<pk>\d+)$',
                login_required(UccFollowUnfollowView.as_view()), name='follow-unfollow-influencer'),

            url(r'^like-unlike-product/(?P<pk>\d+)$',
                login_required(ProductLikeUnlikeView.as_view()), name='like-unlike-product'),

            url(r'followed-creators/$',
                login_required(InfluencerView.as_view()), name='followed-creators'),

            url(r'^unfollow-creator/(?P<pk>\d+)$',
                login_required(InfluencerUnfollowView.as_view()), name='unfollow-creator'),

            url(r'^liked-products/$',
                login_required(ProductsView.as_view()), name='liked-products'),

            url(r'^my-payments/$',
                login_required(BankcardView.as_view()), name='my-payments'),

            url(r'^my-payments/delete/(?P<pk>\d+)$',
                login_required(BankcardDeleteView.as_view()), name='my-payments-delete'),

            url(r'^notifications/settings/$',
                login_required(NotificationsSettingsView.as_view()), name='notifications-settings'),

        ]

        return self.post_process_urls(urls)


application = CustomerApplication()

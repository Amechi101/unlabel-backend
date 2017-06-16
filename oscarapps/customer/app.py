from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from oscar.apps.customer.app import CustomerApplication as CoreCustomerApplication
from oscar.core.application import Application
from oscar.core.loading import get_class
from oscarapps.customer.views import BrandView, BrandUnfollowView, InfluencerView, InfluencerUnfollowView, ProductsView, BankcardView, BankcardDeleteView

class CustomerApplication(CoreCustomerApplication):

    def get_urls(self):

        urls = super(CustomerApplication,self).get_urls()
        urls += [
            url(r'^followed-brands/$',
                login_required(BrandView.as_view()),name='followed-brands'),

            url(r'^unfollow-brand/(?P<pk>\d+)$',
                login_required(BrandUnfollowView.as_view()),name='unfollow-brand'),

            url(r'followed-creators/$',
                login_required(InfluencerView.as_view()),name='followed-creators'),

            url(r'^unfollow-creator/(?P<pk>\d+)$',
                login_required(InfluencerUnfollowView.as_view()),name='unfollow-creator'),

            url(r'^liked-products/$',
                login_required(ProductsView.as_view()),name='liked-products'),

            url(r'^my-payments/$',
                login_required(BankcardView.as_view()),name='my-payments'),

            url(r'^my-payments/delete/(?P<pk>\d+)$',
                login_required(BankcardDeleteView.as_view()),name='my-payments-delete'),

        ]

        return self.post_process_urls(urls)

application = CustomerApplication()

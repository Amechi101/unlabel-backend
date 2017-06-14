from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from oscar.apps.customer.app import CustomerApplication as CoreCustomerApplication
from oscar.core.application import Application
from oscar.core.loading import get_class
from oscarapps.customer.views import BrandView,BrandUnfollowView

class CustomerApplication(CoreCustomerApplication):

    def get_urls(self):

        urls = super(CustomerApplication,self).get_urls()
        urls += [
            url(r'^followed-brands/$',
                login_required(BrandView.as_view()),name='followed-brands'),
            url(r'^unfollow-brand/(?P<pk>\d+)$',
                login_required(BrandUnfollowView.as_view()),name='unfollow-brand'),

             url(r'^addresses/(?P<pk>\d+)/delete/$',
                login_required(self.address_delete_view.as_view()),
                name='address-delete'),

            url(r'followed-creators/$',
                login_required(self.wishlists_list_view.as_view()),name='followed-creators'),
        ]

        return self.post_process_urls(urls)

application = CustomerApplication()

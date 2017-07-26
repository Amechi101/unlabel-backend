from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from oscar.apps.checkout.app import CheckoutApplication as CoreCheckoutApplication
from .views import CheckoutProcess


class CheckoutApplication(CoreCheckoutApplication):

    def get_urls(self):

        urls = super(CheckoutApplication,self).get_urls()
        urls += [
            url(r'^checkout-process/$',
                login_required(CheckoutProcess.as_view()),name='checkout-process'),

        ]

        return self.post_process_urls(urls)

application = CheckoutApplication()

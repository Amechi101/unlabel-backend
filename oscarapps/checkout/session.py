from decimal import Decimal as D

from django import http
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from oscar.core import prices
from oscar.core.compat import user_is_authenticated
from oscar.core.loading import get_class, get_model

# from . import exceptions
from oscar.apps.checkout import exceptions

Repository = get_class('shipping.repository', 'Repository')
OrderTotalCalculator = get_class(
    'checkout.calculators', 'OrderTotalCalculator')
CheckoutSessionData = get_class(
    'checkout.utils', 'CheckoutSessionData')
ShippingAddress = get_model('order', 'ShippingAddress')
BillingAddress = get_model('order', 'BillingAddress')
UserAddress = get_model('address', 'UserAddress')

from oscar.apps.checkout.session import CheckoutSessionMixin as CoreCheckoutSessionMixin


class CheckoutSessionMixin(CoreCheckoutSessionMixin):


    def check_shipping_data_is_captured(self, request):
        if not request.basket.is_shipping_required():
            # Even without shipping being required, we still need to check that
            # a shipping method code has been set.
            if not self.checkout_session.is_shipping_method_set(
                    self.request.basket):
                print("----------------------------1")
                raise exceptions.FailedPreCondition(
                    url=reverse('checkout:checkout-process'),
                )
            return

        # Basket requires shipping: check address and method are captured and
        # valid.
        self.check_a_valid_shipping_address_is_captured()
        self.check_a_valid_shipping_method_is_captured()

    def check_a_valid_shipping_address_is_captured(self):
        # Check that shipping address has been completed
        if not self.checkout_session.is_shipping_address_set():
            print("----------------------------2")
            # raise exceptions.FailedPreCondition(
            #     url=reverse('checkout:checkout-process'),
            #     message=_("Please choose a shipping address")
            # )

        # Check that the previously chosen shipping address is still valid
        shipping_address = self.get_shipping_address(
            basket=self.request.basket)
        if not shipping_address:
            print("----------------------------3")
            # raise exceptions.FailedPreCondition(
            #     url=reverse('checkout:checkout-process'),
            #     message=_("Your previously chosen shipping address is "
            #               "no longer valid.  Please choose another one")
            # )

    def check_a_valid_shipping_method_is_captured(self):
        # Check that shipping method has been set
        # if not self.checkout_session.is_shipping_method_set(
        #         self.request.basket):
        #     print("----------------------------4")
        #     raise exceptions.FailedPreCondition(
        #         url=reverse('checkout:checkout-process'),
        #         message=_("Please choose a shipping method")
        #     )

        # Check that a *valid* shipping method has been set
        shipping_address = self.get_shipping_address(
            basket=self.request.basket)
        shipping_method = self.get_shipping_method(
            basket=self.request.basket,
            shipping_address=shipping_address)
        if not shipping_method:
            print("----------------------------5")
            # raise exceptions.FailedPreCondition(
            #     url=reverse('checkout:checkout-process'),
            #     message=_("Your previously chosen shipping method is "
            #               "no longer valid.  Please choose another one")
            # )



    def skip_unless_basket_requires_shipping(self, request):
        # Check to see that a shipping address is actually required.  It may
        # not be if the basket is purely downloads
        if not request.basket.is_shipping_required():
            print("----------------------------6")
            raise exceptions.PassedSkipCondition(
                url=reverse('checkout:checkout-process')
            )




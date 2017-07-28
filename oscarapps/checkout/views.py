import logging
from django.http import HttpResponseRedirect , Http404
from django.template import RequestContext
import stripe
from django import http
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import six
from django.contrib.auth import login
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views import generic
from django.utils.http import urlquote

from oscar.apps.checkout.views import ThankYouView as CoreThankYouView
from oscar.apps.checkout.views import IndexView as CoreIndexView
from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from oscar.apps.payment import forms, models
from oscarapps.payment.models import CommissionConfiguration,InfluencerCommission,BrandCommission,UnlabelCommission
from oscar.apps.payment.models import Bankcard
from oscar.apps.order.models import Order
from oscar.apps.basket.models import Line
from oscarapps.influencers.models import InfluencerProductReserve
from unlabel import base_settings
from oscar.core.loading import get_class, get_classes, get_model
from oscar.apps.checkout import signals


ShippingAddressForm, ShippingMethodForm, GatewayForm \
    = get_classes('checkout.forms', ['ShippingAddressForm', 'ShippingMethodForm', 'GatewayForm'])
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')
BillingAddress = get_model('order', 'BillingAddress')
BillingAddressForm = get_class('payment.forms', 'BillingAddressForm')
OrderShipingAddress = get_model('order', 'shippingaddress')
UserShipingAddress = get_model('address', 'UserAddress')
OrderPlacementMixin = get_class('checkout.mixins', 'OrderPlacementMixin')
Repository = get_class('shipping.repository', 'Repository')
RedirectRequired, UnableToTakePayment, PaymentError \
    = get_classes('payment.exceptions', ['RedirectRequired',
                                         'UnableToTakePayment',
                                         'PaymentError'])
UnableToPlaceOrder = get_class('order.exceptions', 'UnableToPlaceOrder')
logger = logging.getLogger('oscar.checkout')


class IndexView(CoreIndexView):
    success_url = reverse_lazy('checkout:checkout-process')

    def form_valid(self, form):
        if form.is_guest_checkout() or form.is_new_account_checkout():
            email = form.cleaned_data['username']
            self.checkout_session.set_guest_email(email)

            # We raise a signal to indicate that the user has entered the
            # checkout process by specifying an email address.
            signals.start_checkout.send_robust(
                sender=self, request=self.request, email=email)

            if form.is_new_account_checkout():
                messages.info(
                    self.request,
                    _("Create your account and then you will be redirected "
                      "back to the checkout process"))
                self.success_url = "%s?next=%s&email=%s" % (
                    reverse('customer:register'),
                    reverse('checkout:checkout-process'),
                    urlquote(email)
                )
        else:
            user = form.get_user()
            login(self.request, user)

            # We raise a signal to indicate that the user has entered the
            # checkout process.
            signals.start_checkout.send_robust(
                sender=self, request=self.request)

        return redirect(self.get_success_url())


##########################################################################################################

class CheckoutProcess(OrderPlacementMixin, generic.TemplateView):
    pre_conditions = [
        'check_basket_is_not_empty',
        'check_basket_is_valid',
        'check_user_email_is_captured',
        'check_shipping_data_is_captured',
        'check_payment_data_is_captured']

    template_name = 'checkout/checkout_process.html'

    def get(self, request, *args, **kwargs):
         return super(CheckoutProcess, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(CheckoutProcess, self).get_context_data(**kwargs)
        ctx['use_shipping'] = False
        user = self.request.user
        shipping_address_obj = UserShipingAddress.objects.filter(user=self.request.user).first()
        if shipping_address_obj:
            ctx['shipping_address_form'] = ShippingAddressForm(instance=shipping_address_obj,prefix='shipping')
        else:
            ctx['shipping_address_form'] = ShippingAddressForm(prefix='shipping')
        ctx['invoice_address_form'] = BillingAddressForm(prefix='invoicing')
        ctx['bankcard_form'] = forms.BankcardForm(prefix='bankcard')
        return ctx

    def post(self,request,*args,**kwargs):
        context = self.get_context_data(**kwargs)
        context_instance = RequestContext(self.request)

        shipping_address_form = ShippingAddressForm(data=self.request.POST,prefix='shipping')
        invoice_address_form = BillingAddressForm(data=self.request.POST, prefix='invoicing')
        bankcard_form = forms.BankcardForm(data=self.request.POST, prefix='bankcard')
        invoice_address_form_valid = False
        if request.POST.get('use_shipping') == None and invoice_address_form.is_valid() :
            invoice_address_form_valid = True
        elif request.POST.get('use_shipping') == 'on':
            invoice_address_form_valid = True


        if shipping_address_form.is_valid() and bankcard_form.is_valid() and invoice_address_form_valid==True:
            shipping_address_obj = UserShipingAddress.objects.filter(user=self.request.user).first()
            if not shipping_address_obj:
                shipping_address_obj = UserShipingAddress()
            shipping_address_obj.user = self.request.user
            shipping_address_obj.is_default_for_shipping = True
            shipping_address_obj.is_default_for_billing = True
            shipping_address_obj.phone_number = shipping_address_form.cleaned_data['phone_number']
            shipping_address_obj.title = shipping_address_form.cleaned_data['title']
            shipping_address_obj.first_name = shipping_address_form.cleaned_data['first_name']
            shipping_address_obj.last_name = shipping_address_form.cleaned_data['last_name']
            shipping_address_obj.line1 = shipping_address_form.cleaned_data['line1']
            shipping_address_obj.line2 = shipping_address_form.cleaned_data['line2']
            shipping_address_obj.line3 = shipping_address_form.cleaned_data['line3']
            shipping_address_obj.state = shipping_address_form.cleaned_data['state']
            shipping_address_obj.postcode = shipping_address_form.cleaned_data['postcode']
            shipping_address_obj.country = shipping_address_form.cleaned_data['country']
            shipping_address_obj.save()


            ###TODO get checkbox value from frontend and update billing address also
            address_fields = dict(
                (k, v) for (k, v) in shipping_address_form.instance.__dict__.items()
                if not k.startswith('_'))
            self.checkout_session.ship_to_new_address(address_fields)

            self._methods = Repository().get_shipping_methods(basket=self.request.basket, user=self.request.user,
                            shipping_addr=self.get_shipping_address(self.request.basket),request=self.request)
            self.checkout_session.use_shipping_method(self._methods[0].code)

            return self.do_place_order(request)

        else:
            context['shipping_address_form'] = shipping_address_form
            context['invoice_address_form'] = invoice_address_form
            context['bankcard_form'] = bankcard_form
            return self.render_to_response(context)


    def do_place_order(self, request):
        # Helper method to check that the hidden forms wasn't tinkered
        # with.
        bankcard_form = forms.BankcardForm(data=request.POST,prefix='bankcard')
        # billing_address_form = forms.BillingAddressForm(request.POST)
        if not all([bankcard_form.is_valid(),
                    # billing_address_form.is_valid()
                    ]):
            messages.error(request, "Invalid submission")
            return HttpResponseRedirect(reverse('checkout:checkout-process'))

        # Attempt to submit the order, passing the bankcard object so that it
        # gets passed back to the 'handle_payment' method below.
        submission = self.build_submission()
        submission['payment_kwargs']['bankcard'] = bankcard_form.bankcard
        # submission['payment_kwargs']['billing_address'] = billing_address_form.cleaned_data
        return self.submit(**submission)

        # self.checkout_session.ship_to_user_address(address)  ###ship to address

    def submit(self, user, basket, shipping_address, shipping_method,  # noqa (too complex (10))
               shipping_charge, billing_address, order_total,
               payment_kwargs=None, order_kwargs=None):
        """
        Submit a basket for order placement.

        The process runs as follows:

         * Generate an order number
         * Freeze the basket so it cannot be modified any more (important when
           redirecting the user to another site for payment as it prevents the
           basket being manipulated during the payment process).
         * Attempt to take payment for the order
           - If payment is successful, place the order
           - If a redirect is required (eg PayPal, 3DSecure), redirect
           - If payment is unsuccessful, show an appropriate error message

        :basket: The basket to submit.
        :payment_kwargs: Additional kwargs to pass to the handle_payment
                         method. It normally makes sense to pass form
                         instances (rather than model instances) so that the
                         forms can be re-rendered correctly if payment fails.
        :order_kwargs: Additional kwargs to pass to the place_order method
        """
        if payment_kwargs is None:
            payment_kwargs = {}
        if order_kwargs is None:
            order_kwargs = {}

        # Taxes must be known at this point
        assert basket.is_tax_known, (
            "Basket tax must be set before a user can place an order")
        assert shipping_charge.is_tax_known, (
            "Shipping charge tax must be set before a user can place an order")

        # We generate the order number first as this will be used
        # in payment requests (ie before the order model has been
        # created).  We also save it in the session for multi-stage
        # checkouts (eg where we redirect to a 3rd party site and place
        # the order on a different request).
        order_number = self.generate_order_number(basket)
        self.checkout_session.set_order_number(order_number)
        logger.info("Order #%s: beginning submission process for basket #%d",
                    order_number, basket.id)

        # Freeze the basket so it cannot be manipulated while the customer is
        # completing payment on a 3rd party site.  Also, store a reference to
        # the basket in the session so that we know which basket to thaw if we
        # get an unsuccessful payment response when redirecting to a 3rd party
        # site.
        self.freeze_basket(basket)
        self.checkout_session.set_submitted_basket(basket)

        # We define a general error message for when an unanticipated payment
        # error occurs.
        error_msg = _("A problem occurred while processing payment for this "
                      "order - no payment has been taken.  Please "
                      "contact customer services if this problem persists")

        signals.pre_payment.send_robust(sender=self, view=self)

        try:
            self.handle_payment(order_number, order_total, **payment_kwargs)
        except RedirectRequired as e:
            # Redirect required (eg PayPal, 3DS)
            logger.info("Order #%s: redirecting to %s", order_number, e.url)
            return http.HttpResponseRedirect(e.url)
        except UnableToTakePayment as e:
            # Something went wrong with payment but in an anticipated way.  Eg
            # their bankcard has expired, wrong card number - that kind of
            # thing. This type of exception is supposed to set a friendly error
            # message that makes sense to the customer.
            msg = six.text_type(e)
            logger.warning(
                "Order #%s: unable to take payment (%s) - restoring basket",
                order_number, msg)
            self.restore_frozen_basket()

            # We assume that the details submitted on the payment details view
            # were invalid (eg expired bankcard).
            return self.render_payment_details(
                self.request, error=msg, **payment_kwargs)
        except PaymentError as e:
            # A general payment error - Something went wrong which wasn't
            # anticipated.  Eg, the payment gateway is down (it happens), your
            # credentials are wrong - that king of thing.
            # It makes sense to configure the checkout logger to
            # mail admins on an error as this issue warrants some further
            # investigation.
            msg = six.text_type(e)
            logger.error("Order #%s: payment error (%s)", order_number, msg,
                         exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=error_msg, **payment_kwargs)
        except Exception as e:
            # Unhandled exception - hopefully, you will only ever see this in
            # development...
            logger.error(
                "Order #%s: unhandled exception while taking payment (%s)",
                order_number, e, exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=error_msg, **payment_kwargs)

        signals.post_payment.send_robust(sender=self, view=self)

        # If all is ok with payment, try and place order
        logger.info("Order #%s: payment successful, placing order",
                    order_number)
        try:
            return self.handle_order_placement(
                order_number, user, basket, shipping_address, shipping_method,
                shipping_charge, billing_address, order_total, **order_kwargs)
        except UnableToPlaceOrder as e:
            # It's possible that something will go wrong while trying to
            # actually place an order.  Not a good situation to be in as a
            # payment transaction may already have taken place, but needs
            # to be handled gracefully.
            msg = six.text_type(e)
            logger.error("Order #%s: unable to place order - %s",
                         order_number, msg, exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=msg, **payment_kwargs)


##########################################################################################################


class PaymentDetailsView(CorePaymentDetailsView):
    """
      Stripe Integration
    """

    def get_context_data(self, **kwargs):
        """
        Add data for Stripe
        """
        # Override method so the bankcard and billing address forms can be
        # added to the context.
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        ctx['bankcard_form'] = kwargs.get(
            'bankcard_form', forms.BankcardForm())
        # ctx['billing_address_form'] = kwargs.get(
        # 'billing_address_form', forms.BillingAddressForm())
        return ctx

    def post(self, request, *args, **kwargs):
        # Override so we can validate the bankcard/billingaddress submission.
        # If it is valid, we render the preview screen with the forms hidden
        # within it.  When the preview is submitted, we pick up the 'action'
        # parameters and actually place the order.
        if request.POST.get('action', '') == 'place_order':
            return self.do_place_order(request)

        bankcard_form = forms.BankcardForm(request.POST)
        # billing_address_form = forms.BillingAddressForm(request.POST)
        if not all([bankcard_form.is_valid(),
                    # billing_address_form.is_valid()
                    ]):
            # Form validation failed, render page again with errors
            self.preview = False
            ctx = self.get_context_data(
                bankcard_form=bankcard_form,
                # billing_address_form=billing_address_form
            )
            return self.render_to_response(ctx)

        # Render preview with bankcard and billing address details hidden
        return self.render_preview(request,
                                   bankcard_form=bankcard_form,
                                   # billing_address_form=billing_address_form
                                   )

    def do_place_order(self, request):
        # Helper method to check that the hidden forms wasn't tinkered
        # with.
        bankcard_form = forms.BankcardForm(request.POST)
        # billing_address_form = forms.BillingAddressForm(request.POST)
        if not all([bankcard_form.is_valid(),
                    # billing_address_form.is_valid()
                    ]):
            messages.error(request, "Invalid submission")
            return HttpResponseRedirect(reverse('checkout:payment-details'))

        # Attempt to submit the order, passing the bankcard object so that it
        # gets passed back to the 'handle_payment' method below.
        submission = self.build_submission()
        submission['payment_kwargs']['bankcard'] = bankcard_form.bankcard
        # submission['payment_kwargs']['billing_address'] = billing_address_form.cleaned_data
        return self.submit(**submission)

    def handle_payment(self, order_number, total, **kwargs):
        """
        Make submission to Stripe
        """
        try:
            stripe.api_key = base_settings.STRIPE_API_KEY
            self.stripe = stripe
            response = self.stripe.Charge.create(
                amount=int(total.incl_tax * 100),
                currency="usd",
                card={
                    "number": kwargs['bankcard'].number,
                    "exp_month": kwargs['bankcard'].expiry_date.strftime("%m"),
                    "exp_year": kwargs['bankcard'].expiry_date.strftime("%Y"),
                    "cvc": kwargs['bankcard'].cvv,
                },
                description="Order Number: " + str(order_number)
            )
            if response["status"] == "succeeded":
                try:
                    source_type, is_created = models.SourceType.objects.get_or_create(
                        name='Stripe')
                    source = source_type.sources.model(
                        source_type=source_type,
                        amount_allocated=total.incl_tax, currency=total.currency, reference=response["id"])
                    self.add_payment_source(source)
                    self.add_payment_event('Authorised', total.incl_tax)
                    bank_card, created = Bankcard.objects.get_or_create(number=kwargs['bankcard'].number,
                                                                        expiry_date=kwargs['bankcard'].expiry_date,
                                                                        user=self.request.user)
                    bank_card.save()
                except:
                    stripe.Refund.create(charge=response["id"])
                    raise self.stripe.CardError
        except:
            raise self.stripe.CardError


class ThankYouView(CoreThankYouView):

    def get_object(self):
        # We allow superusers to force an order thank-you page for testing
        order = None
        if self.request.user.is_superuser:
            if 'order_number' in self.request.GET:
                order = Order._default_manager.get(
                    number=self.request.GET['order_number'])
            elif 'order_id' in self.request.GET:
                order = Order._default_manager.get(
                    id=self.request.GET['order_id'])

        if not order:
            if 'checkout_order_id' in self.request.session:
                order = Order._default_manager.get(
                    pk=self.request.session['checkout_order_id'])
            else:
                raise Http404(_("No order found"))
        try:
            if order:
                commission_conf = CommissionConfiguration.objects.all().first()
                lines = Line.objects.filter(basket=order.basket)
                if not InfluencerCommission.objects.filter(order=order) or \
                        (not BrandCommission.objects.filter(order=order)) or \
                        (not UnlabelCommission.objects.filter(order=order)):
                    unlabel_commission_total = 0
                    for line in lines:
                            brand_commission_obj, created = BrandCommission.objects.get_or_create(brand=line.product.brand, order=order)
                            if brand_commission_obj.amount is None:
                                brand_commission_obj.amount = (((line.price_incl_tax*commission_conf.brand_commission)
                                                        /100)*line.quantity)
                            else:
                                brand_commission_obj.amount += (((line.price_incl_tax*commission_conf.brand_commission)
                                                            /100)*line.quantity)
                            brand_commission_obj.save()
                            influencer_prod_res = InfluencerProductReserve.objects.get(product=line.product)
                            influencer_commission_obj, created = InfluencerCommission.objects.get_or_create(influencer=influencer_prod_res.influencer, order=order)
                            if influencer_commission_obj.amount is None:
                                influencer_commission_obj.amount = (((line.price_incl_tax*commission_conf.influencer_commission)
                                                        /100)*line.quantity)
                            else:
                                influencer_commission_obj.amount += (((line.price_incl_tax*commission_conf.influencer_commission)
                                                        /100)*line.quantity)
                            influencer_commission_obj.save()
                            unlabel_commission_total += (((line.price_incl_tax*commission_conf.unlabel_commission)
                                                              /100)*line.quantity)
                    unlabel_commission_obj, created = UnlabelCommission.objects.get_or_create(order=order)
                    unlabel_commission_obj.amount = unlabel_commission_total
                    unlabel_commission_obj.save()
        except Exception as e:
             return order
        return order
from django.contrib import messages
from django.http import HttpResponseRedirect , Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.views import generic

import stripe
from oscar.apps.checkout.views import ThankYouView as CoreThankYouView
from oscar.apps.checkout.views import IndexView as CoreIndexView
from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from oscar.apps.payment import forms, models
from oscarapps.payment.models import CommissionConfiguration,InfluencerCommission,BrandCommission,UnlabelCommission

from oscar.apps.payment.models import Bankcard
from oscar.apps.order.models import Order
from oscar.apps.basket.models import Line
from oscarapps.influencers.models import InfluencerProductReserve
from oscar.core.loading import get_class, get_classes, get_model

from unlabel import base_settings
from .forms import InvoiceAddressForm

ShippingAddressForm, ShippingMethodForm, GatewayForm \
    = get_classes('checkout.forms', ['ShippingAddressForm', 'ShippingMethodForm', 'GatewayForm'])
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')
BillingAddress = get_model('order', 'BillingAddress')
BillingAddressForm = get_class('payment.forms', 'BillingAddressForm')


class IndexView(CoreIndexView):
    success_url = reverse_lazy('checkout:checkout-process')

##########################################################################################################

class CheckoutProcess(CheckoutSessionMixin,generic.TemplateView):
    template_name = 'checkout/checkout_process.html'

    def get_context_data(self, **kwargs):
        ctx = super(CheckoutProcess, self).get_context_data(**kwargs)
        ctx['use_shipping'] = True
        ctx['invoice_address_form'] = BillingAddressForm
        ctx['shipping_address_form'] = ShippingAddressForm
        ctx['bankcard_form'] = forms.BankcardForm()
        return ctx

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
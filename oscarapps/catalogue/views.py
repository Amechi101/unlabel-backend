from django.http import HttpResponsePermanentRedirect
from django.utils.http import urlquote
from django.views.generic import DetailView

from oscar.apps.catalogue.signals import product_viewed
from oscar.core.compat import user_is_authenticated
from oscar.core.loading import get_class, get_model
from oscarapps.influencers.models import Influencers, InfluencerProductReserve
from users.models import User


Product = get_model('catalogue', 'product')
Category = get_model('catalogue', 'category')
ProductAlert = get_model('customer', 'ProductAlert')
ProductAlertForm = get_class('customer.forms', 'ProductAlertForm')
get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')



class ProductDetailView(DetailView):
    context_object_name = 'product'
    model = Product
    view_signal = product_viewed
    template_folder = "catalogue"

    # Whether to redirect to the URL with the right path
    enforce_paths = True

    # Whether to redirect child products to their parent's URL
    enforce_parent = True

    def get(self, request, **kwargs):
        """

        Ensures that the correct URL is used before rendering a response
        """
        self.object = product = self.get_object()
        # if product.structure != 'child':
        #     inf_res = InfluencerProductReserve.objects.get(product=product,is_live=True)
        #     inf = Influencers.objects.get(pk=inf_res.influencer.pk)


        redirect = self.redirect_if_necessary(request.path, product)
        if redirect is not None:
            return redirect

        response = super(ProductDetailView, self).get(request, **kwargs)

        # context = self.get_context_data(object=self.object)
        # context.update({'influencer':inf})
        self.send_signal(request, response, product)
        return response

    def get_object(self, queryset=None):
        # Check if self.object is already set to prevent unnecessary DB calls
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ProductDetailView, self).get_object(queryset)

    def redirect_if_necessary(self, current_path, product):
        if self.enforce_parent and product.is_child:
            return HttpResponsePermanentRedirect(
                product.parent.get_absolute_url())

        if self.enforce_paths:
            expected_path = product.get_absolute_url()
            if expected_path != urlquote(current_path):
                return HttpResponsePermanentRedirect(expected_path)

    def get_context_data(self, **kwargs):
        ctx = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.get_object()
        if product.structure != 'child':
            try:
                inf_res = InfluencerProductReserve.objects.get(product=product,is_live=True)
                inf = Influencers.objects.get(pk=inf_res.influencer.pk)
                ctx['influencer'] = inf
            except:
                pass
        ctx['alert_form'] = self.get_alert_form()
        ctx['has_active_alert'] = self.get_alert_status()
        return ctx

    def get_alert_status(self):
        # Check if this user already have an alert for this product
        has_alert = False
        if user_is_authenticated(self.request.user):
            alerts = ProductAlert.objects.filter(
                product=self.object, user=self.request.user,
                status=ProductAlert.ACTIVE)
            has_alert = alerts.exists()
        return has_alert

    def get_alert_form(self):
        return ProductAlertForm(
            user=self.request.user, product=self.object)

    def send_signal(self, request, response, product):
        self.view_signal.send(
            sender=self, product=product, user=request.user, request=request,
            response=response)

    def get_template_names(self):
        """
        Return a list of possible templates.

        If an overriding class sets a template name, we use that. Otherwise,
        we try 2 options before defaulting to catalogue/detail.html:
            1). detail-for-upc-<upc>.html
            2). detail-for-class-<classname>.html

        This allows alternative templates to be provided for a per-product
        and a per-item-class basis.
        """
        if self.template_name:
            return [self.template_name]

        return [
            '%s/detail-for-upc-%s.html' % (
                self.template_folder, self.object.upc),
            '%s/detail-for-class-%s.html' % (
                self.template_folder, self.object.get_product_class().slug),
            '%s/detail.html' % (self.template_folder)]



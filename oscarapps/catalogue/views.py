from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect
from django.utils.http import urlquote
from django.views.generic import DetailView

from oscar.apps.catalogue.signals import product_viewed
from oscar.core.compat import user_is_authenticated
from oscar.core.loading import get_class, get_model
from oscarapps.influencers.models import Influencers, InfluencerProductReserve
from users.models import User
from oscar.apps.catalogue.views import ProductDetailView as CoreProductDetailView


Product = get_model('catalogue', 'product')
Category = get_model('catalogue', 'category')
ProductAlert = get_model('customer', 'ProductAlert')
ProductAlertForm = get_class('customer.forms', 'ProductAlertForm')
get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')
UserProductLike = get_model('customer','UserProductLike')

Line = get_class('basket.models','Line')
LineAttribute = get_class('basket.models','LineAttribute')
ProductAttribute = get_class('catalogue.models','ProductAttribute')
ProductAttributeValue = get_class('catalogue.models','ProductAttributeValue')



class ProductDetailView(CoreProductDetailView):
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
        if product.structure == 'parent':
            child_products = Product.objects.filter(parent=product)
            for child in child_products:
                try:
                    inf_reserved = InfluencerProductReserve.objects.get(product=child)
                    reserved_product = child
                    break
                except:
                    pass
            try:
                attr_value = ProductAttributeValue.objects.get(product=reserved_product,attribute__code__iexact='size')
                size = attr_value.value_option
            except:
                size = ''
            ctx['influencer_size'] = size
            ctx['influencer'] = product.influencer

        elif product.structure == 'standalone':
            try:
                inf_res = InfluencerProductReserve.objects.get(product=product,is_live=True)
            except:
                pass
            try:
                attr_value = ProductAttributeValue.objects.get(product=inf_res.product,attribute__code__iexact='size')
                size = attr_value.value_option
            except:
                size = ''
            ctx['influencer'] = product.influencer
            ctx['influencer_size'] = size

        if not self.request.user.is_anonymous():
            try:
                product_liked = UserProductLike.objects.get(user=self.request.user,product_like=product)
                ctx['user_liked'] = True
            except ObjectDoesNotExist:
                ctx['user_liked'] = False

        ctx['alert_form'] = self.get_alert_form()
        ctx['has_active_alert'] = self.get_alert_status()

        # try:
        #     product_categories = product.categories.all()
        #     sibling_categories = []
        #     for category in product_categories:
        #         sibling_categories.append(category.get_siblings())
        #
        #     sibling_categories = list(set(sibling_categories))
        #     promoted_products = []
        #
        #     for sibling in sibling_categories:
        #         try:
        #             promoted_products.append(Product.objects.filter(status='L',categories__in=sibling).exclude(id=product.id))
        #         except:
        #             pass
        #     flat_promoted_products = [item for sublist in promoted_products for item in sublist]
        #     if len(flat_promoted_products) < 3:
        #         prods = Product.objects.filter(Q(structure='parent')|Q(structure='standalone')).order_by('date_created')[:3-len(flat_promoted_products)]
        #         for prod in prods:
        #             flat_promoted_products.append(prod)
        # except:
        #     flat_promoted_products = Product.objects.filter(Q(structure='parent')|Q(structure='standalone')).order_by('date_created')[:3]

        # ctx['promoted_products'] = flat_promoted_products

        brand_products = Product.objects.filter(brand=product.brand)
        filtered_products = brand_products.filter(Q(structure='parent')|Q(structure='standalone')).order_by('date_created')[:3]
        ctx['promoted_products'] = filtered_products


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



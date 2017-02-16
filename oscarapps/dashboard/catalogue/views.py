from oscarapps.dashboard.catalogue.forms import InfluencerProductImageFormSet
from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as \
    CoreProductCreateUpdateView
from oscar.apps.dashboard.catalogue.views import ProductListView as CoreProductListView
from oscar.apps.dashboard.catalogue.views import ProductSearchForm, ProductClassSelectForm, ProductTable, Product
from django.utils.translation import ugettext_lazy as _
from oscar.apps.dashboard.catalogue.views import ProductDeleteView as \
    CoreProductDeleteView

class ProductCreateUpdateView(CoreProductCreateUpdateView):
    influencer_product_image_formset = InfluencerProductImageFormSet

    def __init__(self, *args, **kwargs):
        super(ProductCreateUpdateView, self).__init__(*args, **kwargs)
        self.formsets = {
            'category_formset': self.category_formset,
            'image_formset': self.image_formset,
            'influencer_product_image_formset': self.influencer_product_image_formset,
            'recommended_formset': self.recommendations_formset,
            'stockrecord_formset': self.stockrecord_formset}

    def get_queryset(self):
        """
        Filter products that the user doesn't have permission to update
        """
        return filter_products(Product.objects.all(), self.request.user)

    def get_form_kwargs(self):
        kwargs = super(ProductCreateUpdateView, self).get_form_kwargs()
        kwargs['product_class'] = self.product_class
        kwargs['parent'] = self.parent
        kwargs['user'] = self.request.user
        return kwargs

def filter_products(queryset, user):
    """
    Restrict the queryset to products the given user has access to.
    A staff user is allowed to access all Products.
    A non-staff user is only allowed access to a product if they are in at
    least one stock record's partner user list.
    """
    if user.is_staff:
        return queryset
    return queryset.filter(brand__users__pk=user.pk).distinct()


class ProductListView(CoreProductListView):

    """
    Dashboard view of the product list.
    Supports the permission-based dashboard.
    """

    template_name = 'dashboard/catalogue/product_list.html'
    form_class = ProductSearchForm
    productclass_form_class = ProductClassSelectForm
    table_class = ProductTable
    context_table_name = 'products'

    def get_context_data(self, **kwargs):
        ctx = super(ProductListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        ctx['productclass_form'] = self.productclass_form_class()
        return ctx

    def get_description(self, form):
        if form.is_valid() and any(form.cleaned_data.values()):
            return _('Product search results')
        return _('Products')

    def get_table(self, **kwargs):
        if 'recently_edited' in self.request.GET:
            kwargs.update(dict(orderable=False))

        table = super(ProductListView, self).get_table(**kwargs)
        table.caption = self.get_description(self.form)
        return table

    def get_table_pagination(self, table):
        return dict(per_page=20)

    def filter_queryset(self, queryset):
        """
        Apply any filters to restrict the products that appear on the list
        """
        return filter_products(queryset, self.request.user)

    def get_queryset(self):
        """
        Build the queryset for this list
        """
        queryset = Product.browsable.base_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.apply_search(queryset)
        return queryset

    def apply_search(self, queryset):
        """
        Filter the queryset and set the description according to the search
        parameters given
        """
        self.form = self.form_class(self.request.GET)

        if not self.form.is_valid():
            return queryset

        data = self.form.cleaned_data

        if data.get('upc'):
            # Filter the queryset by upc
            # If there's an exact match, return it, otherwise return results
            # that contain the UPC
            matches_upc = Product.objects.filter(upc=data['upc'])
            qs_match = queryset.filter(
                Q(id__in=matches_upc.values('id')) |
                Q(id__in=matches_upc.values('parent_id')))

            if qs_match.exists():
                queryset = qs_match
            else:
                matches_upc = Product.objects.filter(upc__icontains=data['upc'])
                queryset = queryset.filter(
                    Q(id__in=matches_upc.values('id')) | Q(id__in=matches_upc.values('parent_id')))

        if data.get('title'):
            queryset = queryset.filter(title__icontains=data['title'])

        return queryset

class ProductDeleteView(CoreProductDeleteView):

    def get_queryset(self):
        """
        Filter products that the user doesn't have permission to update
        """
        print ("fffffffffffffffffffffffffff")
        return Product.objects.all()

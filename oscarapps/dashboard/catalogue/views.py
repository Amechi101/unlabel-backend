from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from oscar.apps.dashboard.catalogue.views import ProductSearchForm, ProductClassSelectForm, ProductTable, Product
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView

from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as \
    CoreProductCreateUpdateView
from oscar.apps.dashboard.catalogue.views import ProductListView as CoreProductListView
from oscar.apps.dashboard.catalogue.views import ProductDeleteView as \
    CoreProductDeleteView
from oscar.apps.catalogue.models import AttributeOption, AttributeOptionGroup
from oscar.core.loading import get_classes
from oscar.views import sort_queryset
from django.views import generic
from oscarapps.dashboard.catalogue.forms import InfluencerProductImageFormSet, AttributeOptionForm, SizeOptionForm, \
    SizeOptionCreateForm
from oscar.core.loading import get_model
from oscarapps.dashboard.catalogue.forms import InfluencerProductImageFormSet
from .forms import ReservedProductSearchForm
InfluencerProductReserve = get_model('influencers', 'InfluencerProductReserve')
Partner = get_model('partner', 'Partner')


ProductTable, CategoryTable \
    = get_classes('oscarapps.dashboard.catalogue.tables',
                  ('ProductTable', 'CategoryTable'))


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
        return Product.objects.all()


class AttributeListView(generic.ListView):
    model = AttributeOptionGroup
    context_object_name = 'option_groups'
    template_name = 'dashboard/catalogue/attribute_options/attribute_options_list.html'
    # form_class = SubCategorySearchForm

    # def get_queryset(self):
    # qs = self.model._default_manager.all()
    #     qs = sort_queryset(qs, self.request, ['name'])
    #     self.description = _("All Brand Specializations")
    #     # We track whether the queryset is filtered to determine whether we
    #     # show the search form 'reset' button.
    #     self.is_filtered = False
    #     self.form = self.form_class(self.request.GET)
    #     if not self.form.is_valid():
    #         return qs
    #     data = self.form.cleaned_data
    #     if data['name']:
    #         qs = qs.filter(name__icontains=data['name'])
    #         self.description = _("Brand Specializations matching '%s'") % data['name']
    #         self.is_filtered = True
    #
    #     return qs

    def get_context_data(self, **kwargs):
        ctx = super(AttributeListView, self).get_context_data(**kwargs)
        # ctx['queryset_description'] = self.description
        # ctx['form'] = self.form
        # ctx['is_filtered'] = self.is_filtered
        return ctx


class AttributeManageView(generic.UpdateView):
    """
    This multi-purpose view renders out a form to edit the partner's details,
    the associated address and a list of all associated users.
    """
    template_name = 'dashboard/catalogue/attribute_options/attribute_options_manage.html'
    form_class = AttributeOptionForm
    success_url = reverse_lazy('dashboard:attribute-options')

    def get_object(self, queryset=None):
        self.sub_category = get_object_or_404(AttributeOptionGroup, pk=self.kwargs['pk'])
        return self.sub_category

    def get_initial(self):
        return {'name': self.sub_category.name}

    def get_context_data(self, **kwargs):
        ctx = super(AttributeManageView, self).get_context_data(**kwargs)
        ctx['sub_category'] = self.sub_category
        ctx['title'] = self.sub_category.name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Size Group '%s' was updated successfully.") %
            self.sub_category.name)
        self.sub_category.name = form.cleaned_data['name']
        self.sub_category.save()
        return super(AttributeManageView, self).form_valid(form)


class AttributeOptionsCreateView(generic.CreateView):
    model = AttributeOptionGroup
    template_name = 'dashboard/catalogue/attribute_options/attribute_options_form.html'
    form_class = AttributeOptionForm
    success_url = reverse_lazy('dashboard:attribute-options')

    def get_context_data(self, **kwargs):
        ctx = super(AttributeOptionsCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new Size Group')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Size Group '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:attribute-options')


class AttributeOptionsDeleteView(generic.DeleteView):
    model = AttributeOptionGroup
    template_name = 'dashboard/catalogue/attribute_options/attribute_options_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Size Group '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:attribute-options')


class OptionsListView(generic.ListView):
    model = AttributeOption
    context_object_name = 'option_groups'
    template_name = 'dashboard/catalogue/size_options/size_options_list.html'
    # form_class = SubCategorySearchForm

    # def get_queryset(self):
    # qs = self.model._default_manager.all()
    #     qs = sort_queryset(qs, self.request, ['name'])
    #     self.description = _("All Brand Specializations")
    #     # We track whether the queryset is filtered to determine whether we
    #     # show the search form 'reset' button.
    #     self.is_filtered = False
    #     self.form = self.form_class(self.request.GET)
    #     if not self.form.is_valid():
    #         return qs
    #     data = self.form.cleaned_data
    #     if data['name']:
    #         qs = qs.filter(name__icontains=data['name'])
    #         self.description = _("Brand Specializations matching '%s'") % data['name']
    #         self.is_filtered = True
    #
    #     return qs

    def get_context_data(self, **kwargs):
        ctx = super(OptionsListView, self).get_context_data(**kwargs)
        # ctx['queryset_description'] = self.description
        # ctx['form'] = self.form
        # ctx['is_filtered'] = self.is_filtered
        return ctx


class OptionManageView(generic.UpdateView):
    """
    This multi-purpose view renders out a form to edit the partner's details,
    the associated address and a list of all associated users.
    """
    template_name = 'dashboard/catalogue/size_options/size_options_manage.html'
    form_class = SizeOptionForm
    success_url = reverse_lazy('dashboard:size-options-list')

    def get_object(self, queryset=None):
        self.sub_category = get_object_or_404(AttributeOption, pk=self.kwargs['pk'])
        return self.sub_category

    def get_initial(self):
        return {'name': self.sub_category.group}

    def get_context_data(self, **kwargs):
        ctx = super(OptionManageView, self).get_context_data(**kwargs)
        ctx['sub_category'] = self.sub_category
        ctx['title'] = self.sub_category.group.name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Size option '%s' for group '%s' was updated successfully.") %
            (self.sub_category.option, self.sub_category.group))
        self.sub_category.option = form.cleaned_data['option']
        self.sub_category.save()
        return super(OptionManageView, self).form_valid(form)


class OptionsCreateView(generic.CreateView):
    model = AttributeOption
    template_name = 'dashboard/catalogue/size_options/size_options_form.html'
    form_class = SizeOptionCreateForm
    success_url = reverse_lazy('dashboard:size-options-list')

    def get_context_data(self, **kwargs):
        ctx = super(OptionsCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new Size Option')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Size Option '%s' for group '%s' was created successfully.") % (
                         self.object.option, self.object.group))
        return reverse('dashboard:size-options-list')


class OptionsDeleteView(generic.DeleteView):
    model = AttributeOption
    template_name = 'dashboard/catalogue/size_options/size_options_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Size option '%s' for group '%s' was deleted successfully.") %
                         (self.object.option, self.object.group))
        return reverse('dashboard:size-options-list')


class ReservedProductsView(ListView):
    model = InfluencerProductReserve
    context_object_name = 'reservedproducts'
    template_name = 'dashboard/catalogue/reserved_product_list.html'
    form_class = ReservedProductSearchForm

    def get_queryset(self):
        self.description = _("All Reserved Products")
        if not self.request.user.is_staff:
            brand = Partner.objects.get(users=self.request.user)
            qs = InfluencerProductReserve.objects.filter(product__brand=brand)
        else:
            qs = InfluencerProductReserve.objects.all()
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs
        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(product__title__icontains=data['name'])
            self.description = _("Reserved products matching '%s'") % data['name']
            self.is_filtered = True
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(ReservedProductsView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx

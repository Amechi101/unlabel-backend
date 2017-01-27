from django.shortcuts import get_object_or_404
# from oscar.apps.dashboard.partners.views import PartnerAddressForm
from oscar.apps.dashboard.partners.forms import UserEmailForm
from django.contrib.auth.models import Permission
from oscar.apps.customer.utils import normalise_email
from oscarapps.partner.models import Partner
from oscarapps.address.models import Locations
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404,redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import FormView
from oscar.core.compat import get_user_model
from oscar.core.loading import get_classes, get_model
from oscar.views import sort_queryset
from oscar.apps.dashboard.partners.views import PartnerManageView as CorePartnerManageView
from oscar.apps.dashboard.partners.views import PartnerListView as CorePartnerListView
from oscar.apps.dashboard.partners.views import PartnerDeleteView as CorePartnerDeleteView
from oscar.apps.dashboard.partners.forms import PartnerAddressForm,PartnerSearchForm
from oscarapps.dashboard.partners.forms import PartnerCreateForm
from oscarapps.partner.models import Partner

from oscarapps.address.states import stateList

User = get_user_model()

# =======
#Partner views
#=======

class PartnerManageView(CorePartnerManageView, FormView):
    form_class = PartnerCreateForm

    def get_object(self, queryset=None):
        self.partner = get_object_or_404(Partner, pk=self.kwargs['pk'])
        return self.partner

    def get_initial(self):
        return {'name': self.partner.name}

    def get_context_data(self, **kwargs):

        ctx = super(PartnerManageView, self).get_context_data(**kwargs)
        ctx['partner'] = self.partner
        ctx['title'] = self.partner.name
        ctx['users'] = self.partner.users.all()
        ctx['states'] = stateList
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Brand '%s' was updated successfully.") %
            self.partner.name)
        self.partner.name = form.cleaned_data['name']
        self.partner.save()
        return super(FormView, self).form_valid(form)


class PartnerAddressManageView(generic.UpdateView):
    template_name = 'dashboard/partners/partner_address_manage.html'
    form_class = PartnerAddressForm

    def get_success_url(self):
        return reverse_lazy('dashboard:partner-manage', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        self.partner = get_object_or_404(Partner, pk=self.kwargs['pk'])
        address = self.partner.location
        # if address is None:
        #     address = self.partner.addresses.model(partner=self.partner)
        return address

    def get_initial(self):
        return {'name': self.partner.name}

    def get_context_data(self, **kwargs):

        ctx = super(PartnerAddressManageView, self).get_context_data(**kwargs)
        ctx['partner'] = self.partner
        ctx['title'] = self.partner.name
        ctx['users'] = self.partner.users.all()
        # ctx['states'] = stateList
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Address of brand  '%s' was updated successfully.") %
            self.partner.name)

        self.partner.location=form.save()
        self.partner.save()
        # locationForm=form.save()
        # locationForm.save()
        return super(PartnerAddressManageView, self).form_valid(form)


class PartnerListView(CorePartnerListView):
    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])
        self.description = _("All brands")
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Brands matching '%s'") % data['name']
            self.is_filtered = True

        return qs


class PartnerDeleteView(CorePartnerDeleteView):
    model = Partner
    template_name = 'dashboard/partners/partner_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Brand '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:partner-list')


class PartnerCreateView(generic.CreateView):
    model = Partner
    template_name = 'dashboard/partners/partner_form.html'
    form_class = PartnerCreateForm
    success_url = reverse_lazy('dashboard:partner-list')

    def get_context_data(self, **kwargs):
        ctx = super(PartnerCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new brand')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Brand '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:partner-list')


#=========================
#Brand Store TypeViews
#==========================

#
# BrandStoreType = get_model('partner', 'BrandStoreType')
# (
#     StoreTypeSearchForm, StoreTypeCreateForm
# ) = get_classes(
#     'dashboard.partners.forms',
#     ['StoreTypeSearchForm', 'StoreTypeCreateForm'], 'oscarapps')
#
#
# class StoreTypeListView(generic.ListView):
#     model = BrandStoreType
#     context_object_name = 'store_types'
#     template_name = 'dashboard/partners/store_types/store_type_list.html'
#     form_class = StoreTypeSearchForm
#
#     def get_queryset(self):
#         qs = self.model._default_manager.all()
#         qs = sort_queryset(qs, self.request, ['name'])
#         self.description = _("All Store Types")
#
#         # We track whether the queryset is filtered to determine whether we
#         # show the search form 'reset' button.
#         self.is_filtered = False
#         self.form = self.form_class(self.request.GET)
#         if not self.form.is_valid():
#             return qs
#
#         data = self.form.cleaned_data
#
#         if data['name']:
#             qs = qs.filter(name__icontains=data['name'])
#             self.description = _("Store Types matching '%s'") % data['name']
#             self.is_filtered = True
#
#         return qs
#
#     def get_context_data(self, **kwargs):
#         ctx = super(StoreTypeListView, self).get_context_data(**kwargs)
#         ctx['queryset_description'] = self.description
#         ctx['form'] = self.form
#         ctx['is_filtered'] = self.is_filtered
#         return ctx
#
#
# class StoreTypeCreateView(generic.CreateView):
#     model = BrandStoreType
#     template_name = 'dashboard/partners/store_types/store_type_form.html'
#     form_class = StoreTypeCreateForm
#     success_url = reverse_lazy('dashboard:store-type-list')
#
#     def get_context_data(self, **kwargs):
#         ctx = super(StoreTypeCreateView, self).get_context_data(**kwargs)
#         ctx['title'] = _('Create new store type')
#         return ctx
#
#     def get_success_url(self):
#         messages.success(self.request,
#                          _("Store type '%s' was created successfully.") %
#                          self.object.name)
#         return reverse('dashboard:store-type-list')
#
#
# class StoreTypeManageView(generic.UpdateView):
#     """
#     This multi-purpose view renders out a form to edit the partner's details,
#     the associated address and a list of all associated users.
#     """
#     template_name = 'dashboard/partners/store_types/store_type_manage.html'
#     form_class = StoreTypeCreateForm
#     success_url = reverse_lazy('dashboard:store-type-list')
#
#     def get_object(self, queryset=None):
#         self.store_type = get_object_or_404(BrandStoreType, pk=self.kwargs['pk'])
#         return self.store_type
#
#     def get_initial(self):
#         return {'name': self.store_type.name}
#
#     def get_context_data(self, **kwargs):
#         ctx = super(StoreTypeManageView, self).get_context_data(**kwargs)
#         ctx['store_type'] = self.store_type
#         ctx['title'] = self.store_type.name
#         return ctx
#
#     def form_valid(self, form):
#         messages.success(
#             self.request, _("Store type '%s' was updated successfully.") %
#             self.store_type.name)
#         self.store_type.name = form.cleaned_data['name']
#         self.store_type.save()
#         return super(StoreTypeManageView, self).form_valid(form)
#
#
# class StoreTypeDeleteView(generic.DeleteView):
#     model = BrandStoreType
#     template_name = 'dashboard/partners/store_types/store_type_delete.html'
#
#     def get_success_url(self):
#         messages.success(self.request,
#                          _("Store type '%s' was deleted successfully.") %
#                          self.object.name)
#         return reverse('dashboard:store-type-list')


#=========================
#Brand Categories Views
#==========================


BrandCategories = get_model('partner', 'Category')
(
    BrandCategorySearchForm, BrandCategoryCreateForm
) = get_classes(
    'dashboard.partners.forms',
    ['BrandCategorySearchForm', 'BrandCategoryCreateForm'], 'oscarapps')


class BrandCategoryListView(generic.ListView):
    model = BrandCategories
    context_object_name = 'brand_categories'
    template_name = 'dashboard/partners/brand_categories/brand_category_list.html'
    form_class = BrandCategorySearchForm

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])
        self.description = _("All Brand Categories")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Brand categories matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(BrandCategoryListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx


class BrandCategoryCreateView(generic.CreateView):
    model = BrandCategories
    template_name = 'dashboard/partners/brand_categories/brand_category_form.html'
    form_class = BrandCategoryCreateForm
    success_url = reverse_lazy('dashboard:brand-category-list')

    def get_context_data(self, **kwargs):
        ctx = super(BrandCategoryCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new brand category')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Brand category '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:brand-category-list')


class BrandCategoryManageView(generic.UpdateView):
    """
    This multi-purpose view renders out a form to edit the partner's details,
    the associated address and a list of all associated users.
    """
    template_name = 'dashboard/partners/brand_categories/brand_category_manage.html'
    form_class = BrandCategoryCreateForm
    success_url = reverse_lazy('dashboard:brand-category-list')

    def get_object(self, queryset=None):
        self.brand_category = get_object_or_404(BrandCategories, pk=self.kwargs['pk'])
        return self.brand_category

    def get_initial(self):
        return {'name': self.brand_category.name}

    def get_context_data(self, **kwargs):
        ctx = super(BrandCategoryManageView, self).get_context_data(**kwargs)
        ctx['store_type'] = self.brand_category
        ctx['title'] = self.brand_category.name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Brand category '%s' was updated successfully.") %
            self.brand_category.name)
        self.brand_category.name = form.cleaned_data['name']
        self.brand_category.save()
        return super(BrandCategoryManageView, self).form_valid(form)


class BrandCategoryDeleteView(generic.DeleteView):
    model = BrandCategories
    template_name = 'dashboard/partners/brand_categories/brand_category_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Brand category '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:brand-category-list')


#=========================
#Brand Styles Views
#==========================


BrandStyle = get_model('partner', 'Style')
(
    BrandStyleSearchForm, BrandStyleCreateForm
) = get_classes(
    'dashboard.partners.forms',
    ['BrandStyleSearchForm', 'BrandStyleCreateForm'], 'oscarapps')


class BrandStyleListView(generic.ListView):
    model = BrandStyle
    context_object_name = 'brand_styles'
    template_name = 'dashboard/partners/brand_styles/brand_style_list.html'
    form_class = BrandStyleSearchForm

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])
        self.description = _("All Brand Styles")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Brand style matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(BrandStyleListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx


class BrandStyleCreateView(generic.CreateView):
    model = BrandStyle
    template_name = 'dashboard/partners/brand_styles/brand_style_form.html'
    form_class = BrandStyleCreateForm
    success_url = reverse_lazy('dashboard:brand-style-list')

    def get_context_data(self, **kwargs):
        ctx = super(BrandStyleCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new brand style')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Brand style '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:brand-style-list')


class BrandStyleManageView(generic.UpdateView):
    """
    This multi-purpose view renders out a form to edit the partner's details,
    the associated address and a list of all associated users.
    """
    template_name = 'dashboard/partners/brand_styles/brand_style_manage.html'
    form_class = BrandStyleCreateForm
    success_url = reverse_lazy('dashboard:brand-style-list')

    def get_object(self, queryset=None):
        self.brand_style = get_object_or_404(BrandStyle, pk=self.kwargs['pk'])
        return self.brand_style

    def get_initial(self):
        return {'name': self.brand_style.name}

    def get_context_data(self, **kwargs):
        ctx = super(BrandStyleManageView, self).get_context_data(**kwargs)
        ctx['store_type'] = self.brand_style
        ctx['title'] = self.brand_style.name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Brand style '%s' was updated successfully.") %
            self.brand_style.name)
        self.brand_style.name = form.cleaned_data['name']
        self.brand_style.save()
        return super(BrandStyleManageView, self).form_valid(form)


class BrandStyleDeleteView(generic.DeleteView):
    model = BrandStyle
    template_name = 'dashboard/partners/brand_styles/brand_style_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Brand style '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:brand-style-list')



class PartnerFilterView(generic.ListView):

    model = Partner
    context_object_name = 'partners'
    template_name = 'dashboard/partners/partner_list.html'
    form_class = PartnerSearchForm

    def get(self, request, *args, **kwargs):
        return super(PartnerFilterView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.all()

        is_active = self.request.GET.get('active')
        created_date = self.request.GET.get('created_date')
        modified_date = self.request.GET.get('modified_date')

        if is_active:
            queryset = queryset.filter(is_active=True)

        if created_date:
            queryset = queryset.filter(created__regex=created_date)

        if modified_date:
            queryset = queryset.filter(modified__regex=modified_date)

        self.description = _("All brands")
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)

        if not self.form.is_valid():
            return queryset
        data = self.form.cleaned_data

        if data['name']:
            queryset = queryset.filter(name__icontains=data['name'])
            self.description = _("Brands matching '%s'") % data['name']
            self.is_filtered = True

        return queryset

    def get_context_data(self, **kwargs):
        ctx = super(PartnerFilterView, self).get_context_data(**kwargs)
        is_active = self.request.GET.get('active')
        created_date = self.request.GET.get('created_date')
        modified_date = self.request.GET.get('modified_date')
        if is_active:
            ctx['active'] = True
        if created_date:
            ctx['created_date'] = created_date
        if modified_date:
            ctx['modified_date'] = modified_date
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx

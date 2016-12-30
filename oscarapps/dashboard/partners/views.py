from oscar.apps.dashboard.partners.views import PartnerManageView as CorePartnerManageView
from oscar.apps.dashboard.partners.views import PartnerListView as CorePartnerListView
from oscar.apps.dashboard.partners.views import PartnerDeleteView as CorePartnerDeleteView
from oscar.apps.dashboard.partners.views import PartnerAddressForm
from oscarapps.dashboard.partners.forms import PartnerCreateForm
from oscarapps.partner.models import Partner
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from oscar.views import sort_queryset
from django.core.urlresolvers import reverse,reverse_lazy
from django.views.generic import FormView


#=======
#Partner views
#=======

class PartnerManageView(CorePartnerManageView, FormView):

    form_class = PartnerCreateForm

    def get_object(self, queryset=None):
        self.partner = get_object_or_404(Partner, pk=self.kwargs['pk'])
        partner_details = self.partner
        return partner_details

    def get_initial(self):
        return {'name': self.partner.name}

    def get_context_data(self, **kwargs):
        ctx = super(PartnerManageView, self).get_context_data(**kwargs)
        ctx['partner'] = self.partner
        ctx['title'] = self.partner.name
        ctx['users'] = self.partner.users.all()
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
        address = self.partner.primary_address
        if address is None:
            address = self.partner.addresses.model(partner=self.partner)
        return address

    def get_initial(self):
        return {'name': self.partner.name}

    def get_context_data(self, **kwargs):
        ctx = super(PartnerAddressManageView, self).get_context_data(**kwargs)
        ctx['partner'] = self.partner
        ctx['title'] = self.partner.name
        ctx['users'] = self.partner.users.all()
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Address of brand  '%s' was updated successfully.") %
            self.partner.name)
        self.partner.name = form.cleaned_data['name']
        self.partner.save()
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


#================
#Influencer views
#================


from oscar.core.loading import get_classes, get_model
Influencers = get_model('influencers', 'Influencers')
(
    InfluencerSearchForm, InfluencerCreateForm
) = get_classes(
    'dashboard.partners.forms',
    ['InfluencerSearchForm', 'InfluencerCreateForm'], 'oscarapps')


class InfluencerListView(generic.ListView):
    model = Influencers

    context_object_name = 'influencers'
    template_name = 'dashboard/partners/influencers/influencer_list.html'
    form_class = InfluencerSearchForm

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])
        self.description = _("All Influencers")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Influencers matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx


class InfluencerCreateView(generic.CreateView):
    model = Influencers
    template_name = 'dashboard/partners/influencers/influencer_form.html'
    form_class = InfluencerCreateForm
    success_url = reverse_lazy('dashboard:influencer-list')

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new influencer')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Influencer '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:influencer-list')

#
class InfluencerManageView(generic.UpdateView):
    """
    This multi-purpose view renders out a form to edit the partner's details,
    the associated address and a list of all associated users.
    """
    template_name = 'dashboard/partners/influencers/influencer_manage.html'
    form_class = InfluencerCreateForm
    success_url = reverse_lazy('dashboard:influencer-list')

    def get_object(self, queryset=None):
        self.style = get_object_or_404(Influencers, pk=self.kwargs['pk'])
        style = self.style
        return style

    def get_initial(self):
        return {'name': self.style.name}

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerManageView, self).get_context_data(**kwargs)
        ctx['partner'] = self.style
        ctx['title'] = self.style.name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Influencer '%s' was updated successfully.") %
            self.style.name)
        self.style.name = form.cleaned_data['name']
        self.style.save()
        return super(InfluencerManageView, self).form_valid(form)


class InfluencerDeleteView(generic.DeleteView):
    model = Influencers
    template_name = 'dashboard/partners/influencers/influencer_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Influencer '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:influencer-list')

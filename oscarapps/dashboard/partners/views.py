from oscar.apps.dashboard.partners.views import PartnerManageView as CorePartnerManageView
from oscar.apps.dashboard.partners.views import PartnerListView as CorePartnerListView
from oscar.apps.dashboard.partners.views import PartnerDeleteView as CorePartnerDeleteView
# from oscar.apps.dashboard.partners.views import PartnerAddressForm
from oscarapps.dashboard.partners.forms import PartnerCreateForm,PartnerAddressForm
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
from oscar.views import sort_queryset
from django.core.urlresolvers import reverse,reverse_lazy
from django.views.generic import FormView
from oscar.core.compat import get_user_model
from oscarapps.address.states import stateList
User = get_user_model()

#=======
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
        locationForm=form.save()
        locationForm.save()
        self.partner.location=locationForm
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




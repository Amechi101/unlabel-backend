from oscar.apps.dashboard.partners.views import PartnerManageView as CorePartnerManageView
from oscar.apps.dashboard.partners.views import PartnerAddressForm
from oscarapps.dashboard.partners.forms import PartnerCreateForm
from oscarapps.partner.models import Partner
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.views import generic


class PartnerManageView(CorePartnerManageView):
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


class PartnerAddressManageView(generic.UpdateView):

    template_name = 'dashboard/partners/partner_address_manage.html'
    form_class = PartnerAddressForm
    # success_url = reverse_lazy('dashboard:partner-manage')

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
            self.request, _("Partner address '%s' was updated successfully.") %
            self.partner.name)
        self.partner.name = form.cleaned_data['name']
        self.partner.save()
        return super(PartnerAddressManageView, self).form_valid(form)
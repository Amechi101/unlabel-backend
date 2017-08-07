import uuid

from django.contrib.auth.models import Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import Context
from django.template import loader

from oscar.core.loading import get_classes
from oscar.views import sort_queryset
from oscar.apps.dashboard.partners.forms import UserEmailForm
from oscar.apps.customer.utils import normalise_email

from users.models import User
from oscarapps.address.models import Locations, States, Country
from users.models import User
from oscarapps.dashboard.influencers.forms import ExistingUserForm
from oscarapps.influencers.models import Influencers, InfluencerInvite, Industry
from oscar.core.loading import get_classes, get_model



# ================
# Influencer views
# ================
(InfluencerSearchForm, InfluencerCreateForm, InfluencerManageForm, IndustrySearchForm) = get_classes('dashboard.influencers.forms',
                                                                                 ['InfluencerSearchForm',
                                                                                  'InfluencerCreateForm',
                                                                                  'InfluencerManageForm',
                                                                                  'IndustrySearchForm'],
                                                                                 'oscarapps')


class InfluencerListView(generic.ListView):
    """
    List all existing influencers
    """
    model = Influencers
    context_object_name = 'influencers'
    template_name = 'influencers/influencer_list.html'
    form_class = InfluencerSearchForm

    def post(self, request, *args, **kwargs):
        invite_email = request.POST.get("invite_email")
        if invite_email is not None and invite_email != "":
            current_site = Site.objects.get_current()
            domain = current_site.domain
            context = {
                'domain': domain,
                'verify_code': str(uuid.uuid1()).replace('-', '').upper()[0:10],
                'user': invite_email,
                'protocol': 'http',
            }
            invite_sent = InfluencerInvite()
            invite_sent.email = context['user']
            invite_sent.code = context['verify_code']

            tosend = context['protocol'] + '://' + context['domain'] + '/influencers/influencer-sign-up/' + context[
                'verify_code'] + '/'
            email = EmailMessage()
            email.subject = "Influencer invitation from Unlabel"
            email.content_subtype = "html"
            tem = loader.get_template('influencers/influencer_email_body.html')
            context = Context({'tosend':tosend})
            body = tem.render(context)
            email.body = body
            email.from_email = "Unlabel App"
            email.to = [invite_email]
            email.send()
            messages.success(
                self.request, "An invitation email was successfully sent to '%s' " % invite_sent.email)
            invite_sent.save()
            return HttpResponseRedirect("/dashboard/influencers/")
        else:
            return HttpResponseRedirect("/dashboard/influencers/")

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])

        self.description = _("All influencers")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = Influencers.objects.filter(users__first_name__icontains=data['name'])
            self.description = _("Influencers matching '%s'") % data['name']
            self.is_filtered = True
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx


class InfluencerCreateView(generic.View):
    """
    Create an influencer
    """
    model = Influencers
    template_name = 'influencers/influencer_form.html'
    form_class = InfluencerCreateForm
    success_url = reverse_lazy('dashboard:influencer-list')

    def get(self, request, *args, **kwargs):
        return render(request, 'influencers/influencer_form.html', {'form': InfluencerCreateForm})

    def post(self, request, *args, **kwargs):
        influencer_form = InfluencerCreateForm(data=request.POST)
        if influencer_form.is_valid():
            influencer_user = User.objects.create(email=influencer_form['email'].value(),
                                                  password=influencer_form['password1'].value(),
                                                  first_name=influencer_form['first_name'].value(),
                                                  last_name=influencer_form['last_name'].value(),
                                                  contact_number=influencer_form['contact_number'].value(),
                                                  is_influencer=True,
                                                  gender=influencer_form.cleaned_data['gender'],
                                                  is_active=influencer_form['is_active'].value(),
            )
            influencer_user.save()
            influencer_user.set_password(influencer_form['password1'].value())
            influencer_user.save()

            location = str(influencer_form['loc'].value()).split(', ')
            city = ", ".join(str(x) for x in location[:-2])
            state = str(location[-2:-1][0])
            if str(location[-1:][0]) == "United States":
                country = "USA"
            else:
                country = str(location[-1:][0])
            influencer_location = Locations.objects.create(city=city,
                                                        state=state,
                                                        country=country,
                                                        is_influencer_location=True,
                                                        )
            influencer_location.save()
            print(influencer_location.id, type(influencer_location))
            influencer_profile = Influencers.objects.create(bio=influencer_form['bio'].value(),
                                                            height=influencer_form['height'].value(),
                                                            chest_or_bust=influencer_form['chest_or_bust'].value(),
                                                            hips=influencer_form['hips'].value(),
                                                            waist=influencer_form['waist'].value(),
                                                            users=influencer_user,
                                                            location=influencer_location,
            )
            if 'image' in request.FILES:
                influencer_profile.image = request.FILES['image']
            influencer_profile.save()

            return HttpResponseRedirect("/dashboard/influencers/")

        else:
            return render(request, 'influencers/influencer_form.html', {'form': influencer_form})


class InfluencerManageView(generic.UpdateView):
    """
    Edit and update an influencer
    """
    template_name = 'influencers/influencer_manage.html'
    form_class = InfluencerManageForm
    success_url = reverse_lazy('dashboard:influencer-list')

    def get_object(self, queryset=None):
        self.influencer = get_object_or_404(Influencers, pk=self.kwargs['pk'])

        return self.influencer

    def get_initial(self):
        return {
                # 'city': self.influencer.location.city,
                # 'state': self.influencer.location.state,
                # 'country': self.influencer.location.country,
                'loc':self.influencer.location,
                'email': self.influencer.users.email,
                'password': self.influencer.users.password,
                'first_name': self.influencer.users.first_name,
                'last_name': self.influencer.users.last_name,
                'is_active': self.influencer.users.is_active
                }

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerManageView, self).get_context_data(**kwargs)
        ctx['influencer'] = self.influencer
        ctx['title'] = self.influencer.users.first_name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Influencer '%s' was updated successfully.") %
            self.influencer.users.first_name)
        return super(InfluencerManageView, self).form_valid(form)


class InfluencerDeleteView(generic.DeleteView):
    """
    Delete an influencer from db
    """
    model = Influencers
    template_name = 'influencers/influencer_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Influencer '%s' was deleted successfully.") %

                         self.object.users.first_name)
        self.object.users.is_active = False
        self.object.users.save()
        return reverse('dashboard:influencer-list')


class InfluencerFilterView(generic.ListView):
    """
    View for filtering influencer models based on active influencer parameter
    """
    model = Influencers
    context_object_name = 'influencers'
    template_name = 'influencers/influencer_list.html'
    form_class = InfluencerSearchForm

    def get(self, request, *args, **kwargs):

        return super(InfluencerFilterView, self).get(request, *args, **kwargs)

    def get_queryset(self):

        queryset = self.model.objects.all()
        is_active = self.request.GET.get('active')

        if is_active:
            queryset = queryset.filter(users__is_active=True)

        self.description = _("All influencers")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return queryset

        data = self.form.cleaned_data
        if data['name']:
            queryset = queryset.filter(name__icontains=data['name'])
            self.description = _("Influencers matching '%s'") % data['name']
            self.is_filtered = True
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerFilterView, self).get_context_data(**kwargs)
        if self.request.GET.get('active'):
            ctx['active'] = True
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered

        return ctx


class InfluencerUserUpdateView(generic.UpdateView):
    """
    Update influencer linked user details
    """
    template_name = 'influencers/influencer_user_form.html'
    form_class = ExistingUserForm

    def get_object(self, queryset=None):
        self.influencer = get_object_or_404(Influencers, pk=self.kwargs['influencer_pk'])
        return get_object_or_404(User,
                                 pk=self.kwargs['user_pk'],
                                 influencers__pk=self.kwargs['influencer_pk'])

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerUserUpdateView, self).get_context_data(**kwargs)
        name = self.object.get_full_name() or self.object.email
        ctx['influencer'] = self.influencer
        ctx['title'] = _("Edit user '%s'") % name
        return ctx

    def get_success_url(self):
        name = self.object.get_full_name() or self.object.email
        messages.success(self.request,
                         _("User '%s' was updated successfully.") % name)
        return reverse('dashboard:influencer-list')


(
    LocationSearchForm, LocationCreateForm, LocationUpdateForm
) = get_classes(
    'dashboard.influencers.forms',
    ['LocationSearchForm', 'LocationCreateForm', 'LocationUpdateForm'], 'oscarapps')


class LocationListView(generic.ListView):
    model = Locations
    context_object_name = 'locations'
    template_name = 'dashboard/address/location_list.html'
    form_class = LocationSearchForm

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['city'])
        self.description = _("All locations")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['city']:
            qs = qs.filter(city__icontains=data['city'])
            self.description = _("Locations matching '%s'") % data['city']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(LocationListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx


class LocationCreateView(generic.View):

    model = Locations
    template_name = 'dashboard/address/location_form.html'
    form_class = LocationCreateForm
    success_url = reverse_lazy('dashboard:location-list')

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/address/location_form.html', {'form': LocationCreateForm})

    def post(self, request, *args, **kwargs):
        location_form = LocationCreateForm(data=request.POST)
        if location_form.is_valid():
            location = str(location_form['loc'].value()).split(', ')
            city = ", ".join(str(x) for x in location[:-2])
            state = str(location[-2:-1][0])
            print(str(location[-1:][0]))
            if str(location[-1:][0]) == "United States":
                country = "USA"
            else:
                country = str(location[-1:][0])
            influencer_location = Locations.objects.create(city=city,
                                                        state=state,
                                                        country=country,
                                                        is_influencer_location=location_form['is_influencer_location'].value(),
                                                        is_brand_location = location_form['is_brand_location'].value(),
                                                        )
            influencer_location.save()
            return HttpResponseRedirect("/dashboard/influencers/location")

        else:
            return render(request, 'dashboard/address/location_form.html', {'form': location_form})


class LocationManageView(generic.UpdateView):
    """
    """
    template_name = 'dashboard/address/location_manage.html'
    form_class = LocationUpdateForm
    success_url = reverse_lazy('dashboard:location-list')

    def get_object(self, queryset=None):
        self.location = get_object_or_404(Locations, pk=self.kwargs['pk'])
        return self.location

    def get_initial(self):
        return {'city': self.location.city}

    def get_context_data(self, **kwargs):
        ctx = super(LocationManageView, self).get_context_data(**kwargs)
        ctx['location'] = self.location
        ctx['title'] = self.location.city
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Location '%s' was updated successfully.") %
            self.location.city)
        self.location.city = form.cleaned_data['city']
        self.location.state = form.cleaned_data['state']
        self.location.country = form.cleaned_data['country']
        self.location.save()
        return super(LocationManageView, self).form_valid(form)


class LocationDeleteView(generic.DeleteView):
    model = Locations
    template_name = 'dashboard/address/location_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Location '%s' was deleted successfully.") %
                         self.object.city)
        return reverse('dashboard:location-list')


class IndustryListView(generic.ListView):
    model = Industry
    context_object_name = 'industries'
    template_name = 'dashboard/influencers/industry_list.html'
    form_class = IndustrySearchForm

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])
        self.description = _("All Influencer Industries")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Industries matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(IndustryListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx

class IndustryCreateView(generic.CreateView):

    model = Industry
    template_name = 'dashboard/influencers/industry_create.html'
    form_class = IndustrySearchForm
    success_url = reverse_lazy('dashboard:influencer-industries-list')


class IndustryEditView(generic.UpdateView):
    template_name = 'dashboard/influencers/industry_create.html'
    form_class = IndustrySearchForm
    success_url = reverse_lazy('dashboard:influencer-industries-list')
    model = Industry


class IndustryDeleteView(generic.DeleteView):
    model = Industry
    template_name = 'dashboard/influencers/industry_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Industry '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:influencer-industries-list')

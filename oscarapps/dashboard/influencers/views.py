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

from oscar.core.loading import get_classes
from oscar.views import sort_queryset
from oscar.apps.dashboard.partners.forms import UserEmailForm
from oscar.apps.customer.utils import normalise_email
from users.models import User
from oscarapps.influencers.models import Influencers,InfluencerInvite




# ================
# Influencer views
# ================

(InfluencerSearchForm, InfluencerCreateForm) = get_classes('dashboard.influencers.forms',
                                                           ['InfluencerSearchForm', 'InfluencerCreateForm'],
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
        print("=======================", invite_email)
        current_site = Site.objects.get_current()
        domain = current_site.domain
        verify_code = str(uuid.uuid1()).replace('-','').upper()[0:10]
        context = {
            'domain': domain,
            'verify_code' : str(uuid.uuid1()).replace('-','').upper()[0:10],
            'user': invite_email,
            'protocol': 'http',
        }
        invite_sent = InfluencerInvite()
        invite_sent.email = context['user']
        invite_sent.code = context['verify_code']

        tosend = context['protocol'] + '://' + context['domain'] + '/influencers/influencer-sign-up/' + context['verify_code'] + '/'
        email = EmailMessage()
        email.subject = "Influencer inviattion from Unlabel"
        email.content_subtype = "html"
        email.body = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><META http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
                        <body>
                        <br><br>
                        You're being invited as influencer at unlabel
                        <br><br>
                        Please fill the form provided at the link :
                        <br><br>
                        """ + tosend + """
                        <br><br>
                        Thank you for using our site!
                        <br/>
                        <br/>
                        <p style='font-size:11px;'><i>*** This is a system generated email; Please do not reply. ***</i></p>
                        </body>
                        </head>
                        </html>"""
        email.from_email = "Unlabel App"
        email.to = [invite_email]
        email.send()
        invite_sent.save()
        return HttpResponseRedirect("/oscar/dashboard/influencers/")


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
                                                  first_name=influencer_form['first_name'].value(),
                                                  last_name=influencer_form['last_name'].value())
            influencer_user.save()
            influencer_user.set_password(influencer_form['password'].value())
            influencer_user.save()
            influencer_profile = Influencers.objects.create(bio=influencer_form['bio'].value(),
                                                            height=influencer_form['height'].value(),
                                                            chest_or_bust=influencer_form['chest_or_bust'].value(),
                                                            hips=influencer_form['hips'].value(),
                                                            waist=influencer_form['waist'].value(),
                                                            users=influencer_user
            )
            if 'image' in request.FILES:
                influencer_profile.image = request.FILES['image']

            influencer_profile.save()

            return HttpResponseRedirect("/oscar/dashboard/influencers/")

        else:
            return render(request, 'influencers/influencer_form.html', {'form': influencer_form})


    def get_context_data(self, **kwargs):
        ctx = super(InfluencerCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new influencer')
        return ctx

    def get_success_url(self):
        print("------------------inside get success url")
        messages.success(self.request,
                         _("Influencer '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:influencer-list')


class InfluencerManageView(generic.DetailView):
    """
    Edit and update an influencer
    """
    template_name = 'influencers/influencer_manage.html'
    # form_class = InfluencerCreateForm
    success_url = reverse_lazy('dashboard:influencer-list')

    def get_object(self, queryset=None):
        self.influencer = get_object_or_404(Influencers, pk=self.kwargs['pk'])
        return self.influencer
        #
        # def get_initial(self):
        # return {'name': self.influencer.users.first_name}

        # def get_context_data(self, **kwargs):
        #     ctx = super(InfluencerManageView, self).get_context_data(**kwargs)
        #     ctx['influencer'] = self.influencer
        #     ctx['title'] = self.influencer.users.first_name
        #     ctx['form'] = self.form_class
        #     return ctx

        # def form_valid(self, form):
        #     messages.success(
        #         self.request, _("Influencer '%s' was updated successfully.") %
        #         self.influencer.name)
        #     self.influencer.name = form.cleaned_data['name']
        #     self.influencer.save()
        #     return super(InfluencerManageView, self).form_valid(form)


class InfluencerDeleteView(generic.DeleteView):
    """
    Delete an influencer from db
    """
    model = Influencers
    template_name = 'influencers/influencer_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Influencer '%s' was deleted successfully.") %
                         self.object.name)
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
            queryset = queryset.filter(is_active=True)

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
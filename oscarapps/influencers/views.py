from __future__ import unicode_literals
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode

from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, View
from django.views.generic.detail import SingleObjectMixin
from django.core.exceptions import ObjectDoesNotExist

from oscarapps.influencers.models import Influencers
from oscarapps.influencers.forms import InfluencerSignUpForm
from oscarapps.address.models import Locations, States, Country
from users.models import User


class InfluencerListView(ListView):
    template_name = 'pages/_influencers.html'

    model = Influencers

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerListView, self).get_context_data(**kwargs)
        ctx['influencer_list'] = Influencers.objects.filter(influencer_isActive=True).order_by('-created')

        return ctx


class InfluencerDetailView(SingleObjectMixin, ListView):
    model = Influencers

    template_name = 'pages/_influencer_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Influencers.objects.all())

        return super(InfluencerDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerDetailView, self).get_context_data(**kwargs)

        ctx['influencer'] = self.object

        return ctx

    def get_queryset(self, **kwargs):
        return self.object



class InfluencerSignUpView(View):
    def get(self, request, code, *args, **kwargs):
        return render(request, 'pages/influencer_register.html', {'user_form': InfluencerSignUpForm})

    def post(self, request, code, *args, **kwargs):
        influencer_form = InfluencerSignUpForm(data=request.POST)
        if influencer_form.is_valid():

            influencer_user = User()
            influencer_user.email = influencer_form.cleaned_data['email']
            influencer_user.first_name = influencer_form.cleaned_data['first_name']
            influencer_user.last_name = influencer_form.cleaned_data['last_name']
            influencer_user.is_influencer = True
            influencer_user.contact_number = influencer_form.cleaned_data['contact_number']
            influencer_user.gender = influencer_form.cleaned_data['gender']
            influencer_user.save()
            influencer_user.set_password(influencer_form.cleaned_data['password1'])
            influencer_user.save()

            influencer_profile = Influencers()
            influencer_profile.bio = influencer_form.cleaned_data['bio']
            influencer_profile.height = influencer_form.cleaned_data['height']
            influencer_profile.chest_or_bust = influencer_form.cleaned_data['chest_or_bust']
            influencer_profile.hips = influencer_form.cleaned_data['hips']
            influencer_profile.waist = influencer_form.cleaned_data['waist']
            if 'image' in request.FILES:
                influencer_profile.profile_image = request.FILES['image']

            try:
                state = States.objects.get(pk=influencer_form['state'].value())
            except ObjectDoesNotExist:
                state = None

            influencer_location = Locations.objects.create(city=influencer_form['city'].value(),
                                                           state=state,
                                                           country=Country.objects.get(
                                                               pk=influencer_form['country'].value()),
            )
            influencer_location.save()
            influencer_profile.location = influencer_location
            influencer_profile.users = User.objects.get(email=influencer_form.cleaned_data['email'] )
            influencer_profile.save()


        else:
            return render(request, 'pages/influencer_register.html', {'user_form': influencer_form})






from __future__ import unicode_literals
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import utc

from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, View
from django.views.generic.detail import SingleObjectMixin
from django.core.exceptions import ObjectDoesNotExist

from oscarapps.influencers.models import Influencers,InfluencerInvite
from oscarapps.influencers.forms import InfluencerSignUpForm
from oscarapps.address.models import Locations, States, Country
from users.models import User


class InfluencerListView(ListView):
    template_name = 'influencers/influencers.html'

    model = Influencers

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerListView, self).get_context_data(**kwargs)
        ctx['influencer_list'] = Influencers.objects.filter(influencer_isActive=True).order_by('-created')

        return ctx


class InfluencerDetailView(SingleObjectMixin, ListView):
    model = Influencers

    template_name = 'influencers/influencer_detail.html'

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
        try:
            influencer_invite = InfluencerInvite.objects.get(code=code,is_used=False)
        except ObjectDoesNotExist:
            return HttpResponse("sorry invalid invite request.")
        if influencer_invite.is_used is True:
            return HttpResponse("sorry, The link is already used")
        elif influencer_invite.is_used is False:
            return render(request, 'pages/influencer_register.html', {'user_form': InfluencerSignUpForm})


    def post(self, request, code, *args, **kwargs):

        influencer_form = InfluencerSignUpForm(data=request.POST)
        try :
            influencer_invite = InfluencerInvite.objects.get(code=code,is_used=False)
            check_date = datetime.datetime.utcnow().replace(tzinfo=utc)
            sent_date = influencer_invite.date_sent
            if (((check_date - sent_date).total_seconds())/60)/60 < 24 and influencer_invite.is_used == False:
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
                    influencer_location = Locations.objects.get(pk=influencer_form['location'].value())
                    # influencer_location = Locations()
                    # influencer_location.city = influencer_form.cleaned_data['city']
                    # influencer_location.state = influencer_form.cleaned_data['state']
                    # influencer_location.country = influencer_form.cleaned_data['country']
                    # influencer_location.save()
                    influencer_profile = Influencers()
                    influencer_profile.bio = influencer_form.cleaned_data['bio']
                    influencer_profile.image = request.FILES['image']
                    influencer_profile.chest_or_bust = influencer_form.cleaned_data['chest_or_bust']
                    influencer_profile.height = influencer_form.cleaned_data['height']
                    influencer_profile.hips = influencer_form.cleaned_data['hips']
                    influencer_profile.waist = influencer_form.cleaned_data['waist']
                    influencer_profile.users = influencer_user
                    influencer_profile.location = influencer_location
                    influencer_profile.save()
                    influencer_invite.is_used = True
                    influencer_invite.save()

                    return HttpResponse("Influencer successfully registered.")
                else:
                    return render(request, 'influencers/influencer_register.html', {'user_form': influencer_form})
            else:
                return HttpResponse("The page you requested is expired.")
        except:
            return HttpResponse("Sorry, The sign up link you requested is already used.")





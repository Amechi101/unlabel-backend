import datetime

from oscarapps.address.models import Locations
from oscarapps.partner.forms import PartnerSignUpForm
from oscarapps.partner.models import PartnerInvite, Partner
from users.models import User

from django.contrib.auth.models import Permission
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import utc
from django.views.generic import View


class PartnerSignUpView(View):
    """
        View for Partner Signup
    """
    def get(self, request, code, *args, **kwargs):
        try:
            partner_invite = PartnerInvite.objects.get(code=code)
        except:
            return HttpResponse("sorry link is used already")
        return render(request, 'pages/partner_register.html', {'user_form': PartnerSignUpForm})

    def post(self, request, code, *args, **kwargs):

        partner_form = PartnerSignUpForm(data=request.POST)

        try:
            partner_invite = PartnerInvite.objects.get(code=code)
            check_date = datetime.datetime.utcnow().replace(tzinfo=utc)
            sent_date = partner_invite.date_sent
            if (((check_date - sent_date).total_seconds())/60)/60 < 24 and partner_invite.is_used == False:
                    if partner_form.is_valid():
                        partner_user = User()
                        partner_user.email = partner_form.cleaned_data['email']
                        partner_user.first_name = partner_form.cleaned_data['first_name']
                        partner_user.last_name = partner_form.cleaned_data['last_name']
                        partner_user.is_influencer = False
                        partner_user.is_brand = True
                        partner_user.contact_number = partner_form.cleaned_data['contact_number']
                        partner_user.gender = partner_form.cleaned_data['gender']
                        partner_user.save()
                        partner_user.set_password(partner_form.cleaned_data['password1'])
                        partner_user.save()

                        dashboard_access_perm = Permission.objects.get(
                            codename='dashboard_access', content_type__app_label='partner')
                        partner_user.user_permissions.add(dashboard_access_perm)
                        partner_user.save()
                        partner_location = Locations.objects.get(pk=partner_form['location'].value())
                        # partner_location.city = partner_form.cleaned_data['city']
                        # partner_location.state = partner_form.cleaned_data['state']
                        # partner_location.country = partner_form.cleaned_data['country']
                        # partner_location.save()
                        partner_brand = Partner()
                        partner_brand.name = partner_form.cleaned_data['name']
                        email = partner_form.cleaned_data['email']
                        partner_user = User.objects.get(email=email)
                        partner_brand.save()
                        partner_brand.users.add(partner_user)
                        partner_brand.name = partner_form.cleaned_data['name']
                        partner_brand.description = partner_form.cleaned_data['description']
                        partner_brand.image = partner_form.cleaned_data['image']
                        partner_brand.location = partner_location
                        partner_brand.style = partner_form.cleaned_data['style']
                        partner_brand.category = partner_form.cleaned_data['category']
                        partner_brand.sub_category = partner_form.cleaned_data['sub_category']
                        partner_brand.save()
                        partner_invite.is_used = True
                        partner_invite.save()

                        return HttpResponse("Partner successfully registered.")
                    else:
                        return render(request, 'pages/partner_register.html', {'user_form': partner_form})
            else:
                return HttpResponse("The link is expired")
        except:
            return HttpResponse("sorry link is used already.")



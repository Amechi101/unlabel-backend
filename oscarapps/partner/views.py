import datetime

from django.contrib.auth.models import Permission
from oscarapps.partner.forms import PartnerSignUpForm
from oscarapps.partner.models import PartnerInvite, Partner
from users.models import User
from oscarapps.address.models import Locations
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import utc
from django.views.generic import View
from scarface.models import Application, Platform, Device, Topic, PushMessage
from scarface.tests import TEST_ARN_TOKEN_APNS


class PartnerSignUpView(View):
    """
        View for Partner Signup
    """
    def get(self, request, code, *args, **kwargs):
        return render(request, 'pages/partner_register.html', {'user_form': PartnerSignUpForm})

    def post(self, request, code, *args, **kwargs):

        partner_form = PartnerSignUpForm(request.POST,request.FILES)

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
                        partner_user.contact_number = partner_form.cleaned_data['contact_number']
                        partner_user.gender = partner_form.cleaned_data['gender']
                        partner_user.save()
                        partner_user.set_password(partner_form.cleaned_data['password1'])
                        partner_user.save()
                        partner_invite.is_used = True
                        partner_invite.save()
                        dashboard_access_perm = Permission.objects.get(
                            codename='dashboard_access', content_type__app_label='partner')
                        partner_user.user_permissions.add(dashboard_access_perm)
                        partner_user.save()

                        partner_location = Locations()
                        partner_location.city = partner_form.cleaned_data['city']
                        partner_location.state = partner_form.cleaned_data['state']
                        partner_location.country = partner_form.cleaned_data['country']
                        partner_location.save()

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





                        app = Application.objects.create(name='test_application')

                        apns_platform = Platform.objects.create(
                            platform='APNS',
                            application=app,
                            arn=TEST_ARN_TOKEN_APNS
                        )

                        apple_device = Device.objects.create(device_id= 'ec04b7235df4a21183f062f51ffa2b975c1eb82e',
                                       push_token = '9F74C3B1E23CF6DAFD0ECC77D2BAFA4B620F75D13B1A98F89ED8C3F9A147A2B2', platform = apns_platform)

                        apple_device.register()

                        topic = Topic.objects.create(
                            name='test_topic',
                            application=app,
                        )

                        print("almost topic")

                        topic.register()

                        print("almost topic  registered ")
                        topic.register_device(apple_device)


                        print("before a message")

                        message = PushMessage(
                            badge_count=1,
                            context='url_alert',
                            context_id='none',
                            has_new_content=True,
                            message="Hello world!",
                            sound="default"
                        )
                        apple_device.send(message)
                        print("hoiiiiiii, success")






                        return HttpResponse("Partner successfully registered.")
                    else:
                        return render(request, 'pages/partner_register.html', {'user_form': partner_form})
            else:
                return HttpResponse("The link is expired")
        except:
            return HttpResponse("sorry link is used already")



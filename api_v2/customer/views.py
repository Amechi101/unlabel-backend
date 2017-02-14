from __future__ import unicode_literals
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode
from django.views.generic import ListView, TemplateView
import json, ast,os
from django.core import serializers
from rest_framework import permissions, authentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from scarface.models import Application, Platform, Device, Topic, PushMessage
from scarface.tests import TEST_ARN_TOKEN_APNS
from .serializers import CustomerRegisterSerializer
from django.core.mail.message import EmailMessage
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
import re
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
import datetime
from api_v2.utils import *



# from oscarapps.customer.models import EmailConfirmation


#######################################push testing

class PartnerSignUpView(View):
    """
        View for Partner Signup
    """
    def get(self, request, *args, **kwargs):

        app = Application.objects.create(name='tester_application7')

        apns_platform = Platform.objects.create(
            platform='APNS_SANDBOX',
            application=app,
            arn="arn:aws:sns:ap-south-1:275431664439:app/APNS_SANDBOX/unlabel_-7"
        )

        apple_device = Device.objects.create(device_id= "ec04b7235df4a21183f062f51ffa2b975c1eb82e",
                       push_token = "9F74C3B1E23CF6DAFD0ECC77D2BAFA4B620F75D13B1A98F89ED8C3F9A147A2B2",platform = apns_platform
        )

        apple_device.register()

        topic = Topic.objects.create(
            name='test_topic',
            application=app,
        )

        topic.register()
        #topic.register_device(arn_device)

        message = PushMessage(
            badge_count=1,
            context='url_alert',
            context_id='none',
            has_new_content=True,
            message="sorry chetta... njn engane parayaan paadillarnu",
            sound="default"
        )
        apple_device.send(message)

        return HttpResponse("Partner successfully registered.")




#######################################push testing ends



class CustomerRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        try:
            if len(str(request.data["first_name"])) != 0 and len(str(request.data["first_name"])) < 30 :
                match=re.search('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',request.data["email"])
                if match:
                    # email_exist = User.objects.filter(email=request.data["email"])
                    email_exist = User.objects.filter(email__iexact = request.data["email"])
                    if not email_exist:
                        serializer = CustomerRegisterSerializer(data = request.data)
                        if serializer.is_valid():
                            serializer.save()

                            mailid = request.data["email"]
                            email = EmailMessage()
                            email.subject = "Registration succesful at unlabel"
                            email.content_subtype = "html"
                            email.body = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><META http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
                                            <body>
                                            <h2>Welcome to unlabel</h2>
                                            <p style = 'font-size:14px;'>Hello,</p>
                                            <p>Your email has been succesfully registered with Unlabel.<br/>
                                            </p>
                                            <br/>
                                            <br/>
                                            Thank you!<br/><br/>
                                            <p style='font-size:11px;'><i>*** This is a system generated email; Please do not reply. ***</i></p>
                                            </body>
                                            </head>
                                            </html>"""
                            email.from_email = "Unlabel App"
                            email.to = [mailid]
                            email.send()
                            newUser = User.objects.get(email = request.data["email"])
                            SaveSendMail(newUser,email.subject,email.body)
                            return Response(serializer.data, status = status.HTTP_201_CREATED)
                        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                    else:
                        content = { "message" : "email already registered" }
                        return Response(content,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                else:
                    content = { "invalid email" }
                    return Response(content,status=status.HTTP_400_BAD_REQUEST)
            else :
                content = { "invalid name. name should be less than 30 characters" }
                return Response(content,status=status.HTTP_400_BAD_REQUEST)
        except:
            content = { "message":"Please validate the data and try again." }
            return Response(content,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class CustomerPasswordUpdateView(APIView):
    authentication = (authentication.SessionAuthentication,)
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        try:
            if request.user.is_authenticated():
                customer=request.user
            # customer=User.objects.get(email=request.data["email"])
            else:
                content = { "message":"Please login first." }
                return Response(content,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            customer.set_password(request.data["password"])
            customer.save()
            content = {"message":"password changed successfully. Please login to continue."}
            request.session.clear()
            request.session.delete()
            request.session = None
            return Response(content,status = status.HTTP_201_CREATED)
        except:
            content = { "message":"given email does not exist." }
            return Response(content,status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class CustomerForgotPassword(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        # if request.data["email"]:
            try:
                if User.objects.filter(email__iexact = request.data["email"]).exists():
                    current_site = Site.objects.get_current()
                    domain = current_site.domain
                    user = User.objects.get(email__iexact = request.data["email"])
                    context = {
                        'domain': domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    try:
                        tosend = context['protocol']+'://'+context['domain']+'/api_v2/reset/'+context['uid'].decode("utf-8")+'/'+context['token']
                        mailid = request.data["email"]
                        email = EmailMessage()
                        email.subject = "Password Reset at unlabel"
                        email.content_subtype = "html"
                        email.body = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><META http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
                                        <body>
                                        <br><br>
                                        You're receiving this email because you requested a password reset for your user account at Unlabel.
                                        <br><br>
                                        Please go to the following page and choose a new password:
                                        <br><br>
                                        """+tosend+"""
                                        <br><br>
                                        Thanks for using our site!
                                        <br/>
                                        <br/>
                                        <p style='font-size:11px;'><i>*** This is a system generated email; Please do not reply. ***</i></p>
                                        </body>
                                        </head>
                                        </html>"""
                        email.from_email = "Unlabel App"
                        email.to = [mailid]
                        email.send()
                        SaveSendMail(user,email.subject,email.body)
                        return Response({'code':'OK'}, status.HTTP_200_OK)
                    except:
                        return Response({'code':'Please try again later'}, status = status.HTTP_400_BAD_REQUEST)
            except:
                content = { "message":"email does not exist" }
                return Response(content,status = status.HTTP_404_NOT_FOUND)

class CustomerProfileUpdateView(APIView):
    authentication = (authentication.SessionAuthentication,)
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        try:
            if request.user.is_authenticated():
                customer = request.user
            # customer = User.objects.get(email = request.data["email"])
            else:
                content = { "message":"Please login first." }
                return Response(content,status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except:
            content = { "message":"given email not authenticated." }
            return Response(content,status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        customer.first_name = request.data["first_name"]
        customer.save()
        content = { "message":"name changed successfully" }
        return Response(content,status = status.HTTP_200_OK)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class CustomerProfileDeleteView(APIView):
    authentication = authentication.SessionAuthentication
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        try :
            if request.user.is_authenticated():
                customer = request.user
            else :
                content = { "message":"Please login first." }
                return Response(content,status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except :
            content = { "message":"given email not authenticated." }
            return Response(content,status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        customer.is_active = False
        customer.save()
        content = { "message":"Account deleted Successfully" }
        return Response(content,status = status.HTTP_200_OK)


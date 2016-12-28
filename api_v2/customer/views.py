from __future__ import unicode_literals
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.views.generic import ListView, TemplateView
import json, ast,os
from django.core import serializers
from rest_framework import permissions, authentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerRegisterSerializer
from django.core.mail.message import EmailMessage
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes

from oscarapps.customer.models import EmailConfirmation


class CustomerRegisterView(APIView):
    # authentication = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        try:
            email_exist = User.objects.filter(email=request.data["email"])
            if not email_exist:
                serializer = CustomerRegisterSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()

                    # mailid=request.data["email"]
                    # email = EmailMessage()
                    # email.subject = "Registration succesfull at unlabel"
                    # email.content_subtype = "html"
                    # email.body = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><META http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
                    #                 <body>
                    #                 <h2>Welcome to unlabel</h2>
                    #                 <p style = 'font-size:14px;'>Hello,</p>
                    #                 <p>Your email has been succesfully registered with Unlabel.<br/>
                    #                 </p>
                    #                 <br/>
                    #                 <br/>
                    #                 Thank you!<br/><br/>
                    #                 <p style='font-size:11px;'><i>*** This is a system generated email; Please do not reply. ***</i></p>
                    #                 </body>
                    #                 </head>
                    #                 </html>"""
                    # email.from_email = "Unlabel App"
                    # email.to=[mailid]
                    # email.send()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                content={"message":"email already registered"}
                return Response(content,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except:
            content={"message":"no data"}
            return Response(content,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

class CustomerPasswordUpdateView(APIView):
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        try:
            customer=User.objects.get(email=request.data["email"])
        except:
            content={"message":"given email does not exist"}
            return Response(content,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        customer.set_password(request.data["password"])
        customer.save()
        content={"message":"password changed successfully"}
        return Response(content,status=status.HTTP_201_CREATED)


class CustomerForgotPassword(APIView):
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        if request.data["email"]:
            print("--------------1")
            if User.objects.filter(email=request.data["email"]).exists():
                print("-------------------2")
                EmailConfirm=EmailConfirmation.objects.create(email=request.data["email"])

                current_site = Site.objects.get_current()
                domain = current_site.domain

                user = User.objects.get(email=request.data["email"])
                context = {
                    'domain': domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                try:
                    print("----------------3")
                    tosend= context['protocol']+'://'+context['domain']+'/api_v2/reset/'+context['uid']+'/'+context['token']

                    mailid=request.data["email"]
                    email = EmailMessage()
                    email.subject = "Password Reset at unlabel"
                    email.content_subtype = "html"
                    email.body = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><META http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
                                    <body>
                                    <br><br>
                                    You're receiving this email because you requested a password reset for your user account at example.com.
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
                    email.to=[mailid]
                    email.send()

                    return Response({'code':'OK'}, status.HTTP_200_OK)
                except:
                    return Response({'code':'Please try again later'}, status=status.HTTP_400_BAD_REQUEST)

        content={"message":"email does not exist"}
        return Response(content,status=status.HTTP_200_OK)


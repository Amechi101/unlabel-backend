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

# from oscarapps.customer.models import EmailConfirmation


class CustomerRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        try:
            # email_exist = User.objects.filter(email=request.data["email"])
            email_exist = User.objects.filter(email__iexact = request.data["email"])
            if not email_exist:
                serializer = CustomerRegisterSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()

                    mailid=request.data["email"]
                    email = EmailMessage()
                    email.subject = "Registration succesfull at unlabel"
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
                    email.to=[mailid]
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
    authentication = (authentication.SessionAuthentication,)
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        try:
            if request.user.is_authenticated():
                customer=request.user
            # customer=User.objects.get(email=request.data["email"])
            else:
                content={"message":"Please login first."}
                return Response(content,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except:
            content={"message":"given email does not exist."}
            return Response(content,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        customer.set_password(request.data["password"])
        customer.save()
        content={"message":"password changed successfully. Please login to continue."}
        request.session.clear()
        request.session.delete()
        request.session = None
        return Response(content,status=status.HTTP_201_CREATED)


class CustomerForgotPassword(APIView):
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        if request.data["email"]:
            if User.objects.filter(email=request.data["email"]).exists():
                # EmailConfirm=EmailConfirmation.objects.create(email=request.data["email"])

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

class CustomerProfileUpdateView(APIView):
    authentication = (authentication.SessionAuthentication,)
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        try:
            if request.user.is_authenticated():
                customer=request.user
            # customer=User.objects.get(email=request.data["email"])
            else:
                content={"message":"Please login first."}
                return Response(content,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except:
            content={"message":"given email does not exist."}
            return Response(content,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        customer.first_name=request.data["first_name"]
        customer.save()
        content={"message":"name changed successfully"}
        return Response(content,status=status.HTTP_200_OK)



##########-----------------------------------added for login
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import APIView

from oscarapi import serializers
from oscarapi.utils import login_and_upgrade_session
from oscarapi.basket import operations
from oscar.core.loading import get_model


__all__ = ('LoginView',)

Basket = get_model('basket', 'Basket')


class LoginView(APIView):
    """
    Api for logging in users.

    DELETE:
    Log the user out by destroying the session.
    Anonymous users will have their cart destroyed as well, because there is
    no way to reach it anymoore

    POST(username, password):
    1. The user will be authenticated. The next steps will only be
       performed is login is succesful. Logging in logged in users results in
       405.
    2. The anonymous cart will be merged with the private cart associated with
       that authenticated user.
    3. A new session will be started, this session identifies the authenticated
       user for the duration of the session, without further need for
       authentication.
    4. The new, merged cart will be associated with this session.
    5. The anonymous session will be terminated.
    6. A response will be issued containing the new session id as a header
       (only when the request contained the session header as well).

    GET (enabled in DEBUG mode only):
    Get the details of the logged in user.
    If more details are needed, use the ``OSCARAPI_USER_FIELDS`` setting to change
    the fields the ``UserSerializer`` will render.
    """
    serializer_class = serializers.LoginSerializer

    def get(self, request, format=None):
        if settings.DEBUG:
            if request.user.is_authenticated():
                ser = serializers.UserSerializer(request.user, many=False)
                return Response(ser.data)
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise MethodNotAllowed('GET')

    def merge_baskets(self, anonymous_basket, basket):
        "Hook to enforce rules when merging baskets."
        basket.merge(anonymous_basket)
        anonymous_basket.delete()

    def post(self, request, format=None):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():

            anonymous_basket = operations.get_anonymous_basket(request)

            user = ser.instance

            # refuse to login logged in users, to avoid attaching sessions to
            # multiple users at the same time.
            if request.user.is_authenticated():
                return Response(
                    {'detail': 'Session is in use, log out first'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED)

            request.user = user

            login_and_upgrade_session(request._request, user)

            # merge anonymous basket with authenticated basket.
            basket = operations.get_user_basket(user)
            if anonymous_basket is not None:
                self.merge_baskets(anonymous_basket, basket)

            operations.store_basket_in_session(basket, request.session)

            return Response("")

        return Response(ser.errors, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, format=None):
        """
        Destroy the session.

        for anonymous users that means having their basket destroyed as well,
        because there is no way to reach it otherwise.
        """
        request = request._request
        if request.user.is_anonymous():
            basket = operations.get_anonymous_basket(request)
            if basket:
                operations.flush_and_delete_basket(basket)

        request.session.clear()
        request.session.delete()
        request.session = None

        return Response("")

class LogoutView(APIView):

    # serializer_class = serializers.LoginSerializer

    def post(self,request,format=None):
        print("-----------------------------------123")
        request = request._request
        if request.user.is_anonymous():
            basket = operations.get_anonymous_basket(request)
            if basket:
                operations.flush_and_delete_basket(basket)

        request.session.clear()
        request.session.delete()
        request.session = None

        return Response("")
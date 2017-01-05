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
from django.core.mail.message import EmailMessage
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from .serializers import UserAddressSerializer



class AddAddressView(APIView):
    authentication = (authentication.SessionAuthentication,)
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        serializer = UserAddressSerializer(data=request.data)

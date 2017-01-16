from __future__ import unicode_literals
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
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
from .serializers import UserAddressSerializer #,StatesSerializer
from oscar.apps.address.models import Country
from oscarapps.address.models import States,Locations
from django.http import HttpResponse


class AddAddressView(APIView):
    authentication = (authentication.SessionAuthentication,)
    http_method_names = ('post',)

    def post(self,request,*args,**kwargs):
        if request.user.is_authenticated():
            customer=request.user
            # customer=User.objects.get(email=request.data["email"])
        else:
            content = { "message":"Please login first." }
            return Response(content,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        serializer = UserAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class GetStatesView(APIView):

    def get(self,request,*args,**kwargs):
        country=request.GET.get('country')
        stateList=[]
        dict={}
        if country == 'US':
            states=States.objects.all()
            values = render_to_string("common/state_select.html", {"states": states})
            return HttpResponse(json.dumps({'html': values}), content_type="application/json")

        #
        #     states=States.objects.all()
        #     for state in states:
        #         dict["key"]=state.id
        #         dict["value"]=state.state
        #         stateList.append(dict)
        #         dict={}
        # return Response(stateList,status=status.HTTP_200_OK)



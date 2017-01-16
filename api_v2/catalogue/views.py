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
from django.utils.encoding import force_bytes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import re
import functools
import itertools
from six.moves import map

from django.contrib import auth
from oscar.core.loading import get_model, get_class
from rest_framework import generics,serializers
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from oscarapi import serializers, permissions
from oscarapi.basket.operations import assign_basket_strategy
from rest_framework import viewsets
from oscarapi.views import basic
from .serializers import PartnerSerializer
from rest_framework import pagination
from oscarapps.customer.models import UserProductLike
from oscarapps.catalogue.models import Product

Selector = get_class('partner.strategy', 'Selector')

__all__ = (
    'BasketList', 'BasketDetail',
    'LineAttributeList', 'LineAttributeDetail',
    'ProductList', 'ProductDetail',
    'ProductPrice', 'ProductAvailability',
    'StockRecordList', 'StockRecordDetail',
    'UserList', 'UserDetail',
    'OptionList', 'OptionDetail',
    'CountryList', 'CountryDetail',
    'PartnerList', 'PartnerDetail',
)

Basket = get_model('basket', 'Basket')
LineAttribute = get_model('basket', 'LineAttribute')
Product = get_model('catalogue', 'Product')
StockRecord = get_model('partner', 'StockRecord')
Option = get_model('catalogue', 'Option')
User = auth.get_user_model()
Country = get_model('address', 'Country')
Partner = get_model('partner', 'Partner')


# class ProductListView(generics.ListAPIView):
#
#     paginate_by=5
#     count=5
#     # pagination_class = pagination.PageNumberPagination
#     queryset = Product.objects.all()
#     serializer_class = serializers.ProductLinkSerializer



class ProductLikeView(APIView):
    '''
    API for a customer liking a product, and
    unliking a product if liked already.
    '''
    http_method_names = ('get')
    authentication = authentication.SessionAuthentication

    def get(self,request,prod_id,*args,**kwargs):
        try :
            if request.user.is_authenticated():
                customer = request.user
            else :
                content = { "message":"Please login first." }
                return Response(content,status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            try :
                Prod = Product.objects.get(id = prod_id)
            except :
                content = { "message":"Invalid Product id." }
                return Response(content,status = status.HTTP_200_OK)
            try :
                prodlike_exists = UserProductLike.objects.get(user = customer,product_like = prod)
            except :
                prodlike = UserProductLike.objects.create(user = customer,product_like = prod)
                prodlike.save()
                Prod.likes = Prod.likes + 1
                content = { "message":"Product Liked" }
                return Response(content,status = status.HTTP_200_OK)
            prodlike_exists.delete()
            Prod.likes = Prod.likes - 1
            content = { "message":"Product Dis-liked" }
            return Response(content,status = status.HTTP_200_OK)
        except :
            content = { "message":"Some error occured. Please try again later" }
            return Response(content,status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class BrandListView(APIView):
    # queryset = Partner.objects.all()
    # serializer_class = serializers.PartnerSerializer

    def get(self, request, *args, **kwargs):
        test=1
        if test==1:
            queryset=Partner.objects.all()
            serializerData=PartnerSerializer(queryset ,many=True)
            return Response(serializerData.data)


class ProductListView(APIView):

    def get(self,request,*args,**kwargs):
        param = 1
        if param == 1:
            queryset=Product.objects.all()
            serializerData=serializers.ProductLinkSerializer
            return Response(serializerData.data)
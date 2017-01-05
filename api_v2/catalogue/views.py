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
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from oscarapi import serializers, permissions
from oscarapi.basket.operations import assign_basket_strategy
from rest_framework import viewsets
from oscarapi.views import basic
from rest_framework import pagination


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


class ProductListView(generics.ListAPIView):

    paginate_by=5
    count=5
    # pagination_class = pagination.PageNumberPagination
    queryset = Product.objects.all()
    serializer_class = serializers.ProductLinkSerializer
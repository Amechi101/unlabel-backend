from __future__ import unicode_literals
from datetime import datetime
from haversine import haversine

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.core.mail.message import EmailMessage
from django.db.models import Max, Q
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import pagination
from oscarapi import permissions

from oscar.core.loading import get_model, get_class
from oscarapps.customer.models import UserProductLike

from .serializers import PartnerSerializer, InfluencerSerializer
from oscarapps.partner.models import PartnerFollow, Style, Category, SubCategory, Partner

from oscarapps.catalogue.models import InfluencerProductImage
from oscarapps.influencers.models import Influencers, InfluencerProductReserve, InfluencerProductUnreserve
from oscarapps.partner.models import PartnerFollow, Style
from oscar.apps.partner.models import StockRecord

from .pagination import ListPagination


class CustomerBrandSearchView(generics.ListAPIView):
    pagination_class = ListPagination
    serializer_class = PartnerSerializer
    http_method_names = ('get',)

    def get_queryset(self,*args,**kwargs):
        search = self.request.GET.get('search')

        if search:
            brands = Partner.objects.filter(name__icontains=search)
        else:
            brands = Partner.objects.all()
        return brands


class CustomerInfluencerSearchView(generics.ListAPIView):
    pagination_class = ListPagination
    serializer_class = InfluencerSerializer

    def get_queryset(self,*args,**kwargs):
        search = self.request.GET.get('search')
        if search:
            influencers = Influencers.objects.filter(name__icontains=search)
        else:
            influencers = Influencers.objects.all()
        return influencers


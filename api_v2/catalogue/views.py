from __future__ import unicode_literals
from rest_framework import permissions, authentication
from rest_framework.views import APIView
from rest_framework import status
from django.contrib import auth
from oscar.core.loading import get_model, get_class
from rest_framework import generics,serializers
from rest_framework.response import Response
from oscarapi import serializers, permissions
from rest_framework import pagination
from oscarapps.customer.models import UserProductLike
from oscarapps.catalogue.models import Product
from .serializers import PartnerSerializer,StoreTypeSerializer
from oscarapps.partner.models import BrandStoreType

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


class BrandListView(generics.ListAPIView):

    pagination_class = pagination.LimitOffsetPagination
    serializer_class = PartnerSerializer

    def get_queryset(self, *args, **kwargs):
        param = self.request.GET.get('param')
        search = self.request.GET.get('search')
        type = self.request.GET.get('type')

        # ZA - sort by a to z
        #AZ - sort by z to a
        #ASC - sort by date ascending
        #DESC - sort by date descending

        if search == None and type == None :
            if param == "ZA":
                queryset = Partner.objects.all().order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.all().order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.all().order_by('-created')
            else:
                queryset = Partner.objects.all().order_by('name')
        elif search == None :
            if param == "ZA":
                queryset = Partner.objects.filter(store_type = type).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(store_type = type).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(store_type = type).order_by('-created')
            else:
                queryset = Partner.objects.filter(store_type = type).order_by('name')
        elif type == None :
            if param == "ZA":
                queryset = Partner.objects.filter(name__icontains = search).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(name__icontains = search).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(name__icontains = search).order_by('-created')
            else:
                queryset = Partner.objects.filter(name__icontains = search).order_by('name')

        return queryset


class ProductListView(generics.ListAPIView):

    pagination_class = pagination.LimitOffsetPagination
    serializer_class = serializers.ProductSerializer

    def get_queryset(self, *args, **kwargs):
        param = self.request.GET.get('param')
        brand_id = self.request.GET.get('brand')
        # if param == 'ASC':
        queryset = Product.objects.filter(brand=brand_id)
        return queryset


    # def get(self,request,*args,**kwargs):
    #     param = 1
    #     if param == 1:
    #         queryset=Product.objects.all()
    #         serializerData=serializers.ProductLinkSerializer
    #         return Response(serializerData.data)



class StoreListView(generics.ListAPIView):

    queryset = BrandStoreType.objects.all()
    serializer_class = StoreTypeSerializer
    paginate_by = None
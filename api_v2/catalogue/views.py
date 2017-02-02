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

from .serializers import PartnerSerializer,StoreTypeSerializer,ProductSerializer
from oscarapps.partner.models import PartnerFollow,Style
from oscarapps.influencers.models import Influencers,InfluencerProductReserve

from oscar.apps.partner.models import StockRecord
# from oscar.apps.basket.models import

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
                prodlike_exists = UserProductLike.objects.get(user = customer,product_like = Prod)
            except :
                prodlike = UserProductLike.objects.create(user = customer,product_like = Prod)
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
    http_method_names = ('get',)

    # ZA - sort by a to z
    #AZ - sort by z to a
    #ASC - sort by date ascending
    #DESC - sort by date descending
    # get the queryset for pagination based on the parameter given from ios
    def get_queryset(self, *args, **kwargs):
        param = self.request.GET.get('param')
        search = self.request.GET.get('search')
        type = self.request.GET.get('type')

        live_brand_id = Product.objects.filter(status = 'L' ).values_list('brand',flat = True)

        if search == None and type == None :
            if param == "ZA":
                queryset = Partner.objects.filter(pk__in = live_brand_id).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(pk__in = live_brand_id).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(pk__in = live_brand_id).order_by('-created')
            else:
                queryset = Partner.objects.filter(pk__in = live_brand_id).order_by('name')
        elif search == None :
            if param == "ZA":
                queryset = Partner.objects.filter(store_type = type, pk__in = live_brand_id).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(store_type = type, pk__in = live_brand_id).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(store_type = type, pk__in = live_brand_id).order_by('-created')
            else:
                queryset = Partner.objects.filter(store_type = type,pk__in = live_brand_id).order_by('name')
        elif type == None :
            if param == "ZA":
                queryset = Partner.objects.filter(pk__in = live_brand_id, name__icontains = search).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(pk__in = live_brand_id, name__icontains = search).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(pk__in = live_brand_id, name__icontains = search).order_by('-created')
            else:
                queryset = Partner.objects.filter(pk__in = live_brand_id, name__icontains = search).order_by('name')

        return queryset


class ProductListView(generics.ListAPIView):
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = ProductSerializer
    http_method_names = ('get',)

    # HL - price high to low
    # LH - price low to high
    # NEW - date newest to old
    # OLD - date oldest to new
    def get_queryset(self, *args, **kwargs):
        brand_id = self.request.GET.get('brand')
        param = self.request.GET.get('param')
        if brand_id == None:
            queryset = Product.objects.filter(status = 'L').order_by('created')
        elif param == None :
            queryset = Product.objects.filter(brand = brand_id, status = 'L').order_by('created')
        elif param == 'New':
            queryset = Product.objects.filter(brand = brand_id, status = 'L' ).order_by('-created')
        elif param == 'OLD':
            queryset = Product.objects.filter(brand = brand_id, status = 'L' ).order_by('created')
        elif param == 'HL':
            prod_id_List = Product.objects.filter(brand = brand_id, status = 'L' ).values_list('id',flat = True)
            prod_Sort_List = StockRecord.objects.filter(product__in = prod_id_List).order_by('price_retail').values_list('product',flat = True)
            queryset = Product.objects.filter(pk__in = prod_Sort_List)
        elif param == "LH":
            prod_id_List = Product.objects.filter(brand = brand_id, status = 'L' ).values_list('id',flat = True)
            prod_Sort_List = StockRecord.objects.filter(product__in = prod_id_List).order_by('-price_retail').values_list('product',flat = True)
            queryset = Product.objects.filter(pk__in = prod_Sort_List)

        return queryset



class StoreListView(generics.ListAPIView):

    queryset = Style.objects.all()
    serializer_class = StoreTypeSerializer
    paginate_by = None



class PartnerFollowView(APIView):
    authentication = authentication.SessionAuthentication
    http_method_names = ('get',)

    def get(self,request,partner_id,*args,**kwargs):
        try :
            if request.user.is_authenticated():
                influencer = request.user
            else :
                content = { "message":"Please login first." }
                return Response(content,status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            try :
                partner = Partner.objects.get(id = partner_id)
            except :
                content = { "message":"Invalid Brand id." }
                return Response(content,status = status.HTTP_200_OK)
            try :
                follow_exists = PartnerFollow.objects.get(customer = influencer,partner = partner)
            except :
                follow_exists = PartnerFollow.objects.create(customer = influencer,partner = partner)
                follow_exists.save()
                content = { "message":"Brand Liked" }
                return Response(content,status = status.HTTP_200_OK)
            follow_exists.delete()
            content = { "message":"Brand unfollowed" }
            return Response(content,status = status.HTTP_200_OK)
        except :
            content = { "message":"Some error occured. Please try again later" }
            return Response(content,status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class InfluencerBrandListView(generics.ListAPIView):

    pagination_class = pagination.LimitOffsetPagination
    serializer_class = PartnerSerializer
    http_method_names = ('get',)

    # ZA - sort by a to z
    #AZ - sort by z to a
    #ASC - sort by date ascending
    #DESC - sort by date descending
    # get the queryset for pagination based on the parameter given from ios
    def get_queryset(self, *args, **kwargs):
        param = self.request.GET.get('param')
        search = self.request.GET.get('search')
        type = self.request.GET.get('type')

        live_brand_id = Product.objects.all().values_list('brand',flat = True)

        if search == None and type == None :
            if param == "ZA":
                queryset = Partner.objects.filter(pk__in = live_brand_id).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(pk__in = live_brand_id).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(pk__in = live_brand_id).order_by('-created')
            else:
                queryset = Partner.objects.filter(pk__in = live_brand_id).order_by('name')
        elif search == None :
            if param == "ZA":
                queryset = Partner.objects.filter(store_type = type, pk__in = live_brand_id).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(store_type = type, pk__in = live_brand_id).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(store_type = type, pk__in = live_brand_id).order_by('-created')
            else:
                queryset = Partner.objects.filter(store_type = type,pk__in = live_brand_id).order_by('name')
        elif type == None :
            if param == "ZA":
                queryset = Partner.objects.filter(pk__in = live_brand_id, name__icontains = search).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(pk__in = live_brand_id, name__icontains = search).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(pk__in = live_brand_id, name__icontains = search).order_by('-created')
            else:
                queryset = Partner.objects.filter(pk__in = live_brand_id, name__icontains = search).order_by('name')

        return queryset

class InfluencerProductListView(generics.ListAPIView):
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = ProductSerializer
    http_method_names = ('get',)

    # HL - price high to low
    # LH - price low to high
    # NEW - date newest to old
    # OLD - date oldest to new
    def get_queryset(self,*args,**kwargs):
        brand_id = self.request.GET.get('brand')
        param = self.request.GET.get('param')
        if brand_id == None:
            queryset = Product.objects.filter(status = 'U').order_by('created')
        if brand_id != None:
            if param == None :
                queryset = Product.objects.filter(brand = brand_id, status = 'U').order_by('created')
            elif param == 'New':
                queryset = Product.objects.filter(brand = brand_id, status = 'U' ).order_by('-created')
            elif param == 'OLD':
                queryset = Product.objects.filter(brand = brand_id, status = 'U' ).order_by('created')
            elif param == 'HL':
                prod_id_List = Product.objects.filter(brand = brand_id, status = 'U' ).values_list('id',flat = True)
                prod_Sort_List = StockRecord.objects.filter(product__in = prod_id_List).order_by('price_retail').values_list('product',flat = True)
                queryset = Product.objects.filter(pk__in = prod_Sort_List)
            elif param == "LH":
                prod_id_List = Product.objects.filter(brand = brand_id, status = 'U' ).values_list('id',flat = True)
                prod_Sort_List = StockRecord.objects.filter(product__in = prod_id_List).order_by('-price_retail').values_list('product',flat = True)
                queryset = Product.objects.filter(pk__in = prod_Sort_List)

        return queryset

class InfluencerReserveProduct(APIView):
    authentication = authentication.SessionAuthentication
    http_method_names = ('post',)

    def post(self,request,product_id,*args,**kwargs):
        try :
            if request.user.is_authenticated():
                influencer_user = request.user
            else :
                content = { "message":"Please login first." }
                return Response(content,status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            try:
                product_to_reserve = Product.objects.get(id = product_id,status = 'U')
            except:
                content = {"message":"Product already reserved"}
                return Response(content,status = status.HTTP_303_SEE_OTHER)

            influencer_product_reserved = InfluencerProductReserve()
            influencer_product_reserved.influencer = influencer_user
            influencer_product_reserved.product = product_to_reserve
            product_to_reserve.status = 'R'
            influencer_product_reserved.save()
            content = {"message":"Product reservered successfully"}
            return Response(content,status = status.HTTP_200_OK)
        except:
            content = {"message":"Please try again after some time"}
            return Response(content,status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


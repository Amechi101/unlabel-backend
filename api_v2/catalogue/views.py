from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.db.models import Max
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import pagination
from oscarapi import permissions

from oscar.core.loading import get_model, get_class
from oscarapps.customer.models import UserProductLike
from .pagination import CustomPagination
from .serializers import SizeSerializer
from oscarapps.partner.models import PartnerFollow, Style
from oscarapps.catalogue.models import InfluencerProductImage
from oscarapps.influencers.models import Influencers, InfluencerProductReserve
from .serializers import PartnerSerializer, StoreTypeSerializer, ProductSerializer, \
    InfluencerBrandProductSerializer, \
    InfluencerProductImagesSerializer, InfluencerImageSerializer, InfluencerProductNoteSerializer
from oscarapps.partner.models import PartnerFollow, Style
from oscarapps.influencers.models import Influencers, InfluencerProductReserve
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


class ProductLikeView(APIView):
    '''
    API for a customer liking a product, and
    unliking a product if liked already.
    '''
    http_method_names = ('get')
    authentication = authentication.SessionAuthentication

    def get(self, request, prod_id, *args, **kwargs):
        try:
            if request.user.is_authenticated():
                customer = request.user
            else:
                content = {"message": "Please login first."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            try:
                Prod = Product.objects.get(id=prod_id)
            except:
                content = {"message": "Invalid Product id."}
                return Response(content, status=status.HTTP_200_OK)
            try:
                prodlike_exists = UserProductLike.objects.get(user=customer, product_like=Prod)
            except:
                prodlike = UserProductLike.objects.create(user=customer, product_like=Prod)
                prodlike.save()
                Prod.likes = Prod.likes + 1
                content = {"message": "Product Liked"}
                return Response(content, status=status.HTTP_200_OK)
            prodlike_exists.delete()
            Prod.likes = Prod.likes - 1
            content = {"message": "Product Dis-liked"}
            return Response(content, status=status.HTTP_200_OK)
        except:
            content = {"message": "Some error occured. Please try again later"}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class BrandListView(generics.ListAPIView):
    '''List of brands with at least one live product'''
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

        live_brand_id = Product.objects.filter(status='L').values_list('brand', flat=True)

        if search == None and type == None:
            if param == "ZA":
                queryset = Partner.objects.filter(pk__in=live_brand_id).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(pk__in=live_brand_id).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(pk__in=live_brand_id).order_by('-created')
            else:
                queryset = Partner.objects.filter(pk__in=live_brand_id).order_by('name')
        elif search == None:
            if param == "ZA":
                queryset = Partner.objects.filter(store_type=type, pk__in=live_brand_id).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(store_type=type, pk__in=live_brand_id).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(store_type=type, pk__in=live_brand_id).order_by('-created')
            else:
                queryset = Partner.objects.filter(store_type=type, pk__in=live_brand_id).order_by('name')
        elif type == None:
            if param == "ZA":
                queryset = Partner.objects.filter(pk__in=live_brand_id, name__icontains=search).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(pk__in=live_brand_id, name__icontains=search).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(pk__in=live_brand_id, name__icontains=search).order_by('-created')
            else:
                queryset = Partner.objects.filter(pk__in=live_brand_id, name__icontains=search).order_by('name')

        return queryset


class ProductListView(generics.ListAPIView):
    '''
    List products based on the brand selected(id)
    '''
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
            queryset = Product.objects.filter(status='L').order_by('created')
        elif param == None:
            queryset = Product.objects.filter(brand=brand_id, status='L').order_by('created')
        elif param == 'New':
            queryset = Product.objects.filter(brand=brand_id, status='L').order_by('-created')
        elif param == 'OLD':
            queryset = Product.objects.filter(brand=brand_id, status='L').order_by('created')
        elif param == 'HL':
            prod_id_List = Product.objects.filter(brand=brand_id, status='L').values_list('id', flat=True)
            prod_Sort_List = StockRecord.objects.filter(product__in=prod_id_List).order_by('price_retail').values_list(
                'product', flat=True)
            queryset = Product.objects.filter(pk__in=prod_Sort_List)
        elif param == "LH":
            prod_id_List = Product.objects.filter(brand=brand_id, status='L').values_list('id', flat=True)
            prod_Sort_List = StockRecord.objects.filter(product__in=prod_id_List).order_by('-price_retail').values_list(
                'product', flat=True)
            queryset = Product.objects.filter(pk__in=prod_Sort_List)

        return queryset


class StoreListView(generics.ListAPIView):
    queryset = Style.objects.all()
    serializer_class = StoreTypeSerializer
    paginate_by = None


class PartnerFollowView(APIView):
    authentication = authentication.SessionAuthentication
    http_method_names = ('get',)

    def get(self, request, partner_id, *args, **kwargs):
        try:
            if request.user.is_authenticated():
                influencer = request.user
            else:
                content = {"message": "Please login first."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            try:
                partner = Partner.objects.get(id=partner_id)
            except:
                content = {"message": "Invalid Brand id."}
                return Response(content, status=status.HTTP_200_OK)
            try:
                follow_exists = PartnerFollow.objects.get(customer=influencer, partner=partner)
            except:
                follow_exists = PartnerFollow.objects.create(customer=influencer, partner=partner)
                follow_exists.save()
                content = {"message": "Brand Liked"}
                return Response(content, status=status.HTTP_200_OK)
            follow_exists.delete()
            content = {"message": "Brand unfollowed"}
            return Response(content, status=status.HTTP_200_OK)
        except:
            content = {"message": "Some error occured. Please try again later"}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class InfluencerBrandListView(generics.ListAPIView):
    '''
    List brands for influencer
    '''
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = PartnerSerializer
    http_method_names = ('get',)

    #ZA - sort by a to z
    #AZ - sort by z to a
    #ASC - sort by date ascending
    #DESC - sort by date descending
    # get the queryset for pagination based on the parameter given from ios
    def get_queryset(self, *args, **kwargs):
        param = self.request.GET.get('param')
        search = self.request.GET.get('search')
        type = self.request.GET.get('type')
        live_brand_id = Product.objects.filter()  #.values_list('brand',flat = True)

        if search == None and type == None:
            if param == "ZA":
                queryset = Partner.objects.all().order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.all().order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.all().order_by('-created')
            else:
                queryset = Partner.objects.all().order_by('name')
        elif search == None:
            if param == "ZA":
                queryset = Partner.objects.filter(store_type=type).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(store_type=type).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(store_type=type).order_by('-created')
            else:
                queryset = Partner.objects.filter(store_type=type).order_by('name')
        elif type == None:
            if param == "ZA":
                queryset = Partner.objects.filter(name__icontains=search).order_by('-name')
            elif param == "DESC":
                queryset = Partner.objects.filter(name__icontains=search).order_by('created')
            elif param == "ASC":
                queryset = Partner.objects.filter(name__icontains=search).order_by('-created')
            else:
                queryset = Partner.objects.filter(name__icontains=search).order_by('name')
        return queryset


class InfluencerProductListView(generics.ListAPIView):
    '''
    List products for influencer based on brand
    '''
    pagination_class = CustomPagination
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
            queryset = Product.objects.filter(status='U').order_by('created')
            return queryset
        if brand_id != None:
            if param == 'OLD':
                prod_id_List = Product.objects.filter(brand=brand_id, status='U').values_list('id', flat=True)
                prod_Sort_List = StockRecord.objects.filter(product__in=prod_id_List).order_by(
                    'date_created').values_list('product', flat=True)
                queryset = Product.objects.filter(pk__in=prod_Sort_List)
                ###sorting the queryset
                item_list = []
                for item in prod_Sort_List:
                    obj = queryset.get(id=item)
                    item_list.append(obj)
                return item_list
            elif param == 'HL':
                prod_id_List = Product.objects.filter(brand=brand_id, status='U').values_list('id', flat=True)
                prod_Sort_List = StockRecord.objects.filter(product__in=prod_id_List).order_by(
                    'price_retail').values_list('product', flat=True)
                queryset = Product.objects.filter(pk__in=prod_Sort_List)
                ###sorting the queryset
                item_list = []
                for item in prod_Sort_List:
                    obj = queryset.get(id=item)
                    item_list.append(obj)
                return item_list

            elif param == "LH":
                prod_id_List = Product.objects.filter(brand=brand_id, status='U').values_list('id', flat=True)
                prod_Sort_List = StockRecord.objects.filter(product__in=prod_id_List).order_by(
                    '-price_retail').values_list('product', flat=True)
                queryset = Product.objects.filter(pk__in=prod_Sort_List)
                ###sorting the queryset
                item_list = []
                for item in prod_Sort_List:
                    obj = queryset.get(id=item)
                    item_list.append(obj)
                return item_list
            else:
                prod_id_List = Product.objects.filter(brand=brand_id, status='U').values_list('id', flat=True)
                prod_Sort_List = StockRecord.objects.filter(product__in=prod_id_List).order_by(
                    '-date_created').values_list('product', flat=True)
                queryset = Product.objects.filter(pk__in=prod_Sort_List)
                ###sorting the queryset
                item_list = []
                for item in prod_Sort_List:
                    obj = queryset.get(id=item)
                    item_list.append(obj)
                return item_list


    def list(self, request, *args, **kwargs):

        influencer_user = request.user
        if influencer_user.is_anonymous() == False:
            try:
                influencer = Influencers.objects.filter(users=influencer_user).count()
                if influencer != 0:
                    profile = True
                else:
                    profile = False
            except ObjectDoesNotExist:
                influencer = None
                profile = False
        elif influencer_user.is_anonymous() == True:
            profile = False

        queryset = self.filter_queryset(self.get_queryset())
        if queryset is not None:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = {'profile': profile, 'data': serializer.data}
                return self.get_paginated_response(data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else :
            return Response(None)


class InfluencerReserveProduct(APIView):
    '''
    View for influencer to reserve a product
    '''
    authentication = authentication.SessionAuthentication
    http_method_names = ('post',)

    def post(self, request, product_id, *args, **kwargs):
        try:
            if request.user.is_authenticated():
                influencer_user = request.user
            else:
                content = {"message": "Please login first."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            try:
                product_to_reserve = Product.objects.get(id=product_id, status='U')
            except:
                content = {"message": "Product already reserved"}
                return Response(content, status=status.HTTP_303_SEE_OTHER)

            influencer_product_reserved = InfluencerProductReserve()
            influencer_product_reserved.influencer = influencer_user
            influencer_product_reserved.product = product_to_reserve
            product_to_reserve.status = 'R'
            influencer_product_reserved.save()
            product_to_reserve.save()
            content = {"message": "Product reservered successfully"}
            return Response(content, status=status.HTTP_200_OK)
        except:
            content = {"message": "Please try again after some time"}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class GetSize(generics.ListAPIView):
    '''
    View to get size list of products
    '''
    http_method_names = ('get')
    serializer_class = SizeSerializer

    def get_queryset(self, *args, **kwargs):
        if self.request.GET.get('size_class'):
            size_class = self.request.GET.get('size_class')
            sizes = Size.objects.filter(size_class=size_class)
            return sizes
        else:
            return Size.objects.all()


class InfluencerReservedProducts(APIView):
    '''
    View for listing reserved products
    based on brands for influencer
    '''
    pagination_class = pagination.LimitOffsetPagination
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get')
    serializer_class = InfluencerBrandProductSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            influencer = Influencers.objects.filter(users=request.user)
            reserved_items = InfluencerProductReserve.objects.filter(influencer=influencer).values_list('product',
                                                                                                        flat=True)
            products_reserved = Product.objects.filter(pk__in=reserved_items, status='R',
                                                       rental_status='NON').values_list('id', flat=True)
            stock_brand = StockRecord.objects.filter(product__in=products_reserved).values_list('partner', flat=True)
            brands = Partner.objects.filter(pk__in=stock_brand)
            influencer_reserved_products = []
            for brand in brands:
                prod_stock = StockRecord.objects.filter(partner=brand, product__in=products_reserved).values_list(
                    'product', flat=True)
                brand_prod = Product.objects.filter(pk__in=prod_stock, rental_status='NON')
                BrandAndProd = {'products': brand_prod, 'brand': brand}
                brand_product_ser = InfluencerBrandProductSerializer(BrandAndProd)
                influencer_reserved_products.append(brand_product_ser.data)
            results_dict = {'results' : influencer_reserved_products}
            return Response(results_dict)


class InfluencerRentedProducts(APIView):
    '''
    View for listing rented products
    based on brands for influencer
    '''
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            influencer = Influencers.objects.filter(users=request.user)
            reserved_items = InfluencerProductReserve.objects.filter(influencer=influencer).values_list('product',
                                                                                                        flat=True)
            products_reserved = Product.objects.filter(pk__in=reserved_items, rental_status='REN').values_list('id',
                                                                                                               flat=True)
            stock_brand = StockRecord.objects.filter(product__in=products_reserved).values_list('partner', flat=True)
            brands = Partner.objects.filter(pk__in=stock_brand)
            influencer_reserved_products = []
            for brand in brands:
                prod_stock = StockRecord.objects.filter(partner=brand, product__in=products_reserved).values_list(
                    'product', flat=True)
                brand_prod = Product.objects.filter(pk__in=prod_stock, rental_status='REN')
                BrandAndProd = {'products': brand_prod, 'brand': brand}
                brand_product_ser = InfluencerBrandProductSerializer(BrandAndProd)
                influencer_reserved_products.append(brand_product_ser.data)
            return Response(influencer_reserved_products)


class InfluencerLiveProducts(APIView):
    '''
    View for listing live products
    based on brands for influencer
    '''
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            influencer = Influencers.objects.filter(users=request.user)
            reserved_items = InfluencerProductReserve.objects.filter(influencer=influencer).values_list('product',
                                                                                                        flat=True)
            products_reserved = Product.objects.filter(pk__in=reserved_items, status='L').values_list('id', flat=True)
            stock_brand = StockRecord.objects.filter(product__in=products_reserved).values_list('partner', flat=True)
            brands = Partner.objects.filter(pk__in=stock_brand)
            influencer_reserved_products = []
            for brand in brands:
                prod_stock = StockRecord.objects.filter(partner=brand, product__in=products_reserved).values_list(
                    'product', flat=True)
                brand_prod = Product.objects.filter(pk__in=prod_stock, status='L')
                BrandAndProd = {'products': brand_prod, 'brand': brand}
                brand_product_ser = InfluencerBrandProductSerializer(BrandAndProd)
                influencer_reserved_products.append(brand_product_ser.data)
            return Response(influencer_reserved_products)


class InfluencerProductImagesView(APIView):
    '''
    View for influencer to view and
    add product images
    '''
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get', 'post')
    serializer_class = InfluencerImageSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            if request.GET.get('prod_id'):
                prod_id = request.GET.get('prod_id')
                try:
                    influencer_product = Product.objects.get(pk=prod_id)
                except ObjectDoesNotExist:
                    content = {'message': "invalid product id"}
                    return Response(content, status=status.HTTP_204_NO_CONTENT)
                if influencer_product.structure == "child":
                    image_for_product = influencer_product.parent
                else:
                    image_for_product = influencer_product
                influencer_prod_images = InfluencerProductImage.objects.filter(product=image_for_product)
                if len(influencer_prod_images) != 0:
                    image_serializer = InfluencerProductImagesSerializer(influencer_prod_images, many=True)
                    return Response(image_serializer.data)
            content = {'message': "invalid product id"}
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        else:
            content = {'message': "Please login as influencer and try again."}
            return Response(content, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            image_ser = self.serializer_class(data=request.data)
            if image_ser.is_valid():
                try:
                    influencer_product = Product.objects.get(pk=image_ser.data['product_id'])
                except ObjectDoesNotExist:
                    content = {'message': "invalid product id"}
                    return Response(content, status=status.HTTP_204_NO_CONTENT)
                if influencer_product.structure == "child":
                    image_for_product = influencer_product.parent
                else:
                    image_for_product = influencer_product
                images_max_order = InfluencerProductImage.objects.filter(product=image_for_product).aggregate(
                    Max('display_order'))
                next_order = images_max_order['display_order__max'] + 1
                new_product_image = InfluencerProductImage()
                new_product_image.original = image_ser.validated_data['image']
                new_product_image.product = image_for_product
                new_product_image.display_order = next_order
                new_product_image.save()
                content = {'message': "image added successfully"}
                return Response(content, status=status.HTTP_200_OK)


class InfluencerProductNote(APIView):
    '''
    View for adding product note and viewing current
    product note
    '''
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get', 'post')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            if request.GET.get('prod_id'):
                prod_id = request.GET.get('prod_id')
                try:
                    influencer_product = Product.objects.get(pk=prod_id)
                except ObjectDoesNotExist:
                    content = {'message': "invalid product id"}
                    return Response(content, status=status.HTTP_204_NO_CONTENT)
                if influencer_product.structure == "child":
                    note_for_product = influencer_product.parent
                else:
                    note_for_product = influencer_product
                note_serializer = InfluencerProductNoteSerializer(note_for_product.influencer_product_note)
                return Response(note_serializer.data)
            content = {'message': "invalid product id"}
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        content = {'message': "Please login as influencer."}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        if request.data['note'] and request.data['prod_id']:
            try:
                product = Product.objects.get(pk=request.data["product_id"])
            except:
                content = {'message': "Invalid product id."}
                return Response(content, status=status.HTTP_204_NO_CONTENT)
            if len(request.data['note']) < 200:
                product.influencer_product_note = request.data['note']
                product.save()
                content = {'message': "Product note successfully saved."}
                return Response(content, status=status.HTTP_200_OK)
            else:
                content = {'message': "Product note max length is 200 charecters."}
                return Response(content, status=status.HTTP_205_RESET_CONTENT)













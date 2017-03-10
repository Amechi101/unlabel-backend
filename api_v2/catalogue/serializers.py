from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from oscarapi.utils import (
    OscarModelSerializer,
    overridable,
    OscarHyperlinkedModelSerializer
)

from oscarapps.partner.models import Partner, Style, Category, PartnerFollow, RentalInformation, StockRecord, \
    SubCategory
from oscarapps.address.models import Locations, States
from oscarapps.influencers.models import Influencers, InfluencerProductReserve
from oscar.apps.partner.models import StockRecord
from oscarapps.catalogue.models import Product, InfluencerProductImage
from oscar.core.loading import get_model, get_class

Selector = get_class('partner.strategy', 'Selector')

Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')
ProductCategory = get_model('catalogue', 'ProductCategory')
ProductAttribute = get_model('catalogue', 'ProductAttribute')
ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
ProductImage = get_model('catalogue', 'ProductImage')
Option = get_model('catalogue', 'Option')
Partner = get_model('partner', 'Partner')


class LocationSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField(source='get_state')

    def get_state(self, obj):
        if obj.state is not None:
            return obj.state.name
        else:
            return None

    class Meta:
        model = Locations
        fields = ('city', 'state', 'country', 'latitude', 'longitude')


class PartnerSerializer(OscarModelSerializer):
    location = LocationSerializer()
    followed = serializers.SerializerMethodField(source='get_followed')
    share_url = serializers.SerializerMethodField()

    def get_share_url(self,obj):
        return "http://35.166.138.246"

    def get_followed(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            inf_user = request.user
            if request.user.is_anonymous() == True:
                return False
            elif request.user.is_anonymous() == False:
                brand_follow = PartnerFollow.objects.filter(customer=inf_user, partner=obj)
                if len(brand_follow) > 0:
                    return True
                else:
                    return False
        else:
            return False

    class Meta:
        model = Partner
        fields = '__all__'


class OptionSerializer(OscarHyperlinkedModelSerializer):
    class Meta:
        model = Option
        fields = overridable('OSCARAPI_OPTION_FIELDS', default=(
            'url', 'id', 'name', 'code', 'type'
        ))


class ProductLinkSerializer(OscarHyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = overridable(
            'OSCARAPI_PRODUCT_FIELDS', default=(
                'url', 'id', 'title'
            ))


class ProductAttributeValueSerializer(OscarModelSerializer):
    name = serializers.StringRelatedField(source="attribute")
    value = serializers.StringRelatedField()

    class Meta:
        model = ProductAttributeValue
        fields = ('name', 'value',)


class ProductImageSerializer(OscarModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class RecommmendedProductSerializer(OscarModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail')

    class Meta:
        model = Product
        fields = overridable(
            'OSCARAPI_RECOMMENDED_PRODUCT_FIELDS', default=('url',))


class AvailabilitySerializer(serializers.Serializer):
    is_available_to_buy = serializers.BooleanField()
    num_available = serializers.IntegerField(required=False)
    message = serializers.CharField()


class BaseProductSerializer(OscarModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail')
    stockrecords = serializers.HyperlinkedIdentityField(
        view_name='product-stockrecord-list')
    attributes = ProductAttributeValueSerializer(
        many=True, required=False, source="attribute_values")
    categories = serializers.StringRelatedField(many=True, required=False)
    product_class = serializers.StringRelatedField(required=False)
    images = ProductImageSerializer(many=True, required=False)
    price = serializers.SerializerMethodField()
    options = OptionSerializer(many=True, required=False)
    recommended_products = RecommmendedProductSerializer(
        many=True, required=False)

    def get_price(self, obj):
        if obj.structure == 'parent':
            child_products = Product.objects.filter(structure='child', parent=obj)
            for child_product in child_products:
                try:
                    child_stock = StockRecord.objects.get(product=child_product)
                    price_retail = child_stock.price_retail
                    return {'price_retail': price_retail}
                except:
                    pass
            return {'price_retail': 0.0 }
        else:
            try:
                base_stock = StockRecord.objects.get(product=obj)
                return {'price_retail': base_stock.price_retail}
            except:
                return {'price_retail': 0.0 }


    class Meta:
        model = Product
        fields = overridable(
            'OSCARAPI_PRODUCTDETAIL_FIELDS',
            default=(
                'url', 'id', 'title', 'description', 'material_info',
                'date_created', 'date_updated', 'recommended_products',
                'attributes', 'categories', 'product_class',
                'stockrecords', 'images', 'price', 'options', ))


class ProductSerializer(OscarModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail')
    stockrecords = serializers.HyperlinkedIdentityField(
        view_name='product-stockrecord-list')
    attributes = ProductAttributeValueSerializer(
        many=True, required=False, source="attribute_values")
    categories = serializers.StringRelatedField(many=True, required=False)
    product_class = serializers.StringRelatedField(required=False)
    images = ProductImageSerializer(many=True, required=False)
    price = serializers.HyperlinkedIdentityField(view_name='product-price')
    availability = serializers.SerializerMethodField(source='get_availability')
    options = OptionSerializer(many=True, required=False)
    recommended_products = RecommmendedProductSerializer(
        many=True, required=False)
    sku = serializers.SerializerMethodField(source='get_sku')
    retail_price = serializers.SerializerMethodField(source='get_retail_price')

    def get_sku(self, obj):
        try:
            stock_record = StockRecord.objects.get(product=obj)
        except ObjectDoesNotExist:
            return False
        return stock_record.partner_sku

    def get_retail_price(self, obj):
        try:
            stock_record = StockRecord.objects.get(product=obj)
        except ObjectDoesNotExist:
            return "0.00"
        return stock_record.price_retail

    def get_availability(self, obj):
        product = obj
        strategy = Selector().strategy()
        ser = AvailabilitySerializer(
            strategy.fetch_for_product(product).availability)
        return ser.data

    class Meta:
        model = Product
        fields = overridable(
            'OSCARAPI_PRODUCTDETAIL_FIELDS',
            default=(
                'url', 'id', 'title', 'description', 'material_info',
                'date_created', 'date_updated', 'recommended_products',
                'attributes', 'categories', 'product_class',
                'stockrecords', 'images', 'price', 'availability', 'options', 'sku', 'retail_price'))


class StoreTypeSerializer(OscarModelSerializer):
    class Meta:
        model = Style
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = '__all__'


class RentalInfoSerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = RentalInformation
        fields = '__all__'


class InfluencerProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    attributes = ProductAttributeValueSerializer(
        many=True, required=False, source="attribute_values")
    share_url = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    material_info = serializers.SerializerMethodField()
    sku = serializers.SerializerMethodField(source='get_sku')

    def get_sku(self, obj):
        try:
            stock_record = StockRecord.objects.get(product=obj)
        except ObjectDoesNotExist:
            return ""
        return stock_record.partner_sku

    def get_material_info(self,obj):
        if obj.structure == 'child':
            desc = obj.parent.material_info
        else:
            desc = obj.material_info
        return desc

    def get_description(self,obj):
        if obj.structure == 'child':
            desc = obj.parent.description
        else:
            desc = obj.description
        return desc

    def get_share_url(self,obj):
        return "http://35.166.138.246/"

    def get_images(self, obj):
        if obj.structure == "child":
            image_for_product = obj.parent
        else:
            image_for_product = obj
        prod_image = ProductImage.objects.filter(product=image_for_product)
        image_serializer = ProductImageSerializer(prod_image, many=True, required=False)
        return image_serializer.data

    def get_price(self, obj):
        try:
            stock = StockRecord.objects.get(product=obj)
        except:
            return 0
        return stock.price_retail


    class Meta:
        model = Product
        fields = ['material_info', 'influencer_product_note', 'weight', 'item_sex_type', 'rental_status',
                  'requires_shipping', 'title', 'description', 'id', 'images', 'price', 'attributes','share_url','sku']


class InfluencerBrandSerializer(serializers.ModelSerializer):
    rental_info = RentalInfoSerializer()

    class Meta:
        model = Partner
        fields = '__all__'


class InfluencerBrandProductSerializer(serializers.Serializer):
    products = InfluencerProductSerializer(many=True)
    brand = InfluencerBrandSerializer()

    def validate(self, attrs):
        return attrs


class InfluencerProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerProductImage
        fields = '__all__'


class InfluencerImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    note = serializers.CharField(required=True)


class InfluencerProductNoteSerializer(serializers.Serializer):
    note = serializers.CharField(required=True, max_length=200)


class InfluencerBrandCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class InfluencerBrandStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = '__all__'


class IdSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, max_length=10)


class InfluecnerBrandSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'




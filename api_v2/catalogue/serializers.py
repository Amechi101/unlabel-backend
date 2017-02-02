from rest_framework import serializers

from oscarapi.utils import (
    OscarModelSerializer,
    overridable,
    OscarHyperlinkedModelSerializer
)
from oscarapps.partner.models import Partner, Style
from oscarapps.address.models import Locations
from oscarapps.catalogue.models import Product
from oscar.core.loading import get_model

Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')
ProductCategory = get_model('catalogue', 'ProductCategory')
ProductAttribute = get_model('catalogue', 'ProductAttribute')
ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
ProductImage = get_model('catalogue', 'ProductImage')
Option = get_model('catalogue', 'Option')
Partner = get_model('partner', 'Partner')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Locations
        fields = '__all__'

class PartnerSerializer(OscarModelSerializer):
    location = LocationSerializer()
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
    availability = serializers.HyperlinkedIdentityField(
        view_name='product-availability')
    options = OptionSerializer(many=True, required=False)
    recommended_products = RecommmendedProductSerializer(
        many=True, required=False)

    class Meta:
        model = Product
        fields = overridable(
            'OSCARAPI_PRODUCTDETAIL_FIELDS',
            default=(
                'url', 'id', 'title', 'description',
                'date_created', 'date_updated', 'recommended_products',
                'attributes', 'categories', 'product_class',
                'stockrecords', 'images', 'price', 'availability', 'options'))

class StoreTypeSerializer(OscarModelSerializer):

    class Meta:
        model = Style
        fields='__all__'

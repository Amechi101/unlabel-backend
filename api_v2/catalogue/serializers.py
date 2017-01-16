from rest_framework import serializers

from oscarapi.utils import (
    OscarModelSerializer,
    overridable,
    OscarHyperlinkedModelSerializer
)
from oscarapps.partner.models import Partner
from oscarapps.address.models import Locations
from oscarapps.catalogue.models import Product

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Locations
        fields = '__all__'

class PartnerSerializer(OscarModelSerializer):
    location = LocationSerializer()
    class Meta:
        model = Partner
        fields = '__all__'

class ProductLinkSerializer(OscarHyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = overridable(
            'OSCARAPI_PRODUCT_FIELDS', default=(
                'url', 'id', 'title'
            ))

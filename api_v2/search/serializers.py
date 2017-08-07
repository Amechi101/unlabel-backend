from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from oscarapi.utils import (
    OscarModelSerializer,
    overridable,
    OscarHyperlinkedModelSerializer
)

from oscarapps.partner.models import Partner, Style, Category, PartnerFollow, RentalInformation, StockRecord, \
    SubCategory, RentalTime
from oscarapps.address.models import Locations, States
from oscarapps.influencers.models import Influencers, InfluencerProductReserve
from oscar.apps.partner.models import StockRecord
from oscarapps.catalogue.models import Product, InfluencerProductImage
from oscar.core.loading import get_model, get_class
from users.models import User


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
    display_string = serializers.SerializerMethodField()

    def get_display_string(self,obj):
        return obj.city + ", " + obj.state +", " + obj.country

    class Meta:
        model = Locations
        fields = ('city', 'state', 'country', 'latitude', 'longitude', 'display_string')


class RentalTimesSerializer(serializers.ModelSerializer):

    class Meta:
        model = RentalTime
        fields = '__all__'


class RentalInfoSerializer(serializers.ModelSerializer):
    rent_time = serializers.SerializerMethodField()

    class Meta:
        model = RentalInformation
        fields = '__all__'

    def get_rent_time(self, obj):
        rental_times = obj.rental_time.all()
        times = RentalTime.objects.filter(pk__in=rental_times)
        return RentalTimesSerializer(times, many=True).data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = '__all__'


class PartnerSerializer(OscarModelSerializer):
    location = LocationSerializer()
    rental_info = RentalInfoSerializer()
    followed = serializers.SerializerMethodField(source='get_followed')
    user = serializers.SerializerMethodField()


    def get_user(self,obj):

        return UserSerializer(obj.users.all()[0],many=False).data

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


class InfluencerSerializer(OscarModelSerializer):
    location = LocationSerializer()
    followed = serializers.SerializerMethodField(source='get_followed')
    user = serializers.SerializerMethodField()


    def get_user(self,obj):

        return UserSerializer(obj.users.all()[0],many=False).data

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
        model = Influencers
        fields = '__all__'
from django.contrib.auth.models import User
from rest_framework import serializers
from oscar.apps.address.models import UserAddress,Country
from oscarapps.address.models import States, Locations


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        # fields = ['user','title','line1']
        fields='__all__'

    # def create(self, validated_data):
    #
    #     customer_add = UserAddress.objects.create()
    #     customer_add.user = self.context['request'].user #validated_data["email"]
    #     customer_add.is_default_for_shipping=True
    #     # customer_add.phone_number=
    #     # customer_add.title=
    #     # customer_add.first_name=
    #     # customer_add.last_name=
    #     # line1
    #     # line2
    #     # line3
    #     # line4
    #
    #
    #
    #     # customer_add.username = validated_data["email"][0:29]
    #     # customer_add.set_password(validated_data["password"])
    #     # customer_add.first_name = validated_data["first_name"]
    #     customer_add.save()
    #
    #     return customer_add


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ['printable_name','pk']


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = States
        fields = ['name', 'pk']

class BrandLocationsSerializer(serializers.ModelSerializer):
    state = StateSerializer()
    country = CountrySerializer()
    display_string = serializers.SerializerMethodField()

    def get_display_string(self,obj):
        display = obj.city + ","
        display = display + str(States.objects.get(pk = obj.state.id).name) + ","
        display = display + Country.objects.get(pk=obj.country.pk).printable_name
        return display

    class Meta:
        model = Locations
        fields = ['city','latitude','longitude','state','country','id','display_string']
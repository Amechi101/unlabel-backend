from django.contrib.auth.models import User
from rest_framework import serializers
from oscar.apps.address.models import UserAddress,Country


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        # fields = ['email','password','first_name']

    def create(self, validated_data):

        customer_add = UserAddress.objects.create()
        customer_add.user = self.context['request'].user #validated_data["email"]
        customer_add.is_default_for_shipping=True
        # customer_add.phone_number=
        # customer_add.title=
        # customer_add.first_name=
        # customer_add.last_name=
        # line1
        # line2
        # line3
        # line4



        # customer_add.username = validated_data["email"][0:29]
        # customer_add.set_password(validated_data["password"])
        # customer_add.first_name = validated_data["first_name"]
        customer_add.save()

        return customer_add
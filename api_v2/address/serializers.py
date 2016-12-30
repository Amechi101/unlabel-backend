from django.contrib.auth.models import User
from rest_framework import serializers
from oscar.apps.address.models import UserAddress,Country


# class UserAddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserAddress
#         fields = ['email','password','first_name']
from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.mail import EmailMessage
# from accounts.models import EmailConfirmation


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password','first_name']

    # email = serializers.EmailField(required=True)
    # username = serializers.CharField(required=True,max_length=30)
    # password = serializers.CharField(required=True,max_length=25)

    def create(self, validated_data):
        # customer=User.objects.create_user(validated_data["email"][0:29],validated_data["email"],validated_data["password"])
        # customer.first_name = validated_data["first_name"]

        customer = User.objects.create()
        customer.email = validated_data["email"]
        customer.username = validated_data["email"][0:29]
        customer.set_password(validated_data["password"])
        customer.first_name = validated_data["first_name"]
        customer.save()

        return customer

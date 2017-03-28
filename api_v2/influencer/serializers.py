from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from oscarapi.utils import overridable
from users.models import User
from oscarapps.influencers.models import Influencers


def field_length(fieldname):
    field = next(
        field for field in User._meta.fields if field.name == fieldname)
    return field.max_length


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = overridable('OSCARAPI_USER_FIELDS', (
            User.USERNAME_FIELD, 'id', 'date_joined',))


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=field_length(User.USERNAME_FIELD), required=True)
    password = serializers.CharField(
        max_length=field_length('password'), required=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('invalid login')
        elif not user.is_active:
            raise serializers.ValidationError(
                'Can not log in as inactive user')
        elif not user.is_influencer:
            raise serializers.ValidationError(
                'Normal Users cannot login via the app.')
        elif user.is_staff and overridable(
                'OSCARAPI_BLOCK_ADMIN_API_ACCESS', True):
            raise serializers.ValidationError(
                'Staff users can not log in via the rest api')

        # set instance to the user so we can use this in the view
        self.instance = user
        return attrs

class InfluencerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields=['contact_number','email','first_name','last_name']

class InfluencerPicAndBioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Influencers
        fields = ['bio', 'image']

class InfluencerPhysicalAttributesSerializer(serializers.ModelSerializer):
    sex = serializers.SerializerMethodField()

    def get_sex(self,obj):
        try:
            inf_user = obj.users
            return inf_user.gender
        except:
            return None

    class Meta:
        model = Influencers
        fields = ['height','chest_or_bust','hips','waist','sex']

class InflencerProfileDetailsSerializer(serializers.ModelSerializer):
    email=serializers.SerializerMethodField()
    first_name=serializers.SerializerMethodField()
    last_name=serializers.SerializerMethodField()

    def get_email(self,obj):
        try:
            inf_user = obj.users
            return inf_user.email
        except:
            return None

    def get_first_name(self,obj):
        try:
            inf_user = obj.users
            return inf_user.first_name
        except:
            return None

    def get_last_name(self,obj):
        try:
            inf_user = obj.users
            return inf_user.last_name
        except:
            return None

    class Meta:
        model=Influencers
        fields=['image','auto_id','email','first_name', 'last_name']
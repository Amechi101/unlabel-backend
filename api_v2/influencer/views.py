from __future__ import unicode_literals

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
import re
from rest_framework import permissions, authentication
from django.core.mail.message import EmailMessage
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework import pagination, generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.core.validators import validate_email
from oscarapi import serializers
from oscarapi.utils import login_and_upgrade_session
from oscarapi.basket import operations
from django.core.exceptions import ValidationError
from oscar.apps.address.models import Country

from api_v2.catalogue.serializers import PartnerSerializer
from oscarapps.address.models import Locations, States

from .pagination import InfluencerListPagination
from api_v2.address.serializers import BrandLocationsSerializer
from users.models import User  # ,UserDevice
# from scarface.models import Application, Platform, Device, Topic, PushMessage
from .serializers import LoginSerializer, InfluencerProfileSerializer, InfluencerPicAndBioSerializer, \
    InfluencerPhysicalAttributesSerializer, InflencerProfileDetailsSerializer, InfluencerStyleSerializer, \
    InfluencerPostStyleSerializer, InfluencerIndustrySerializer, InfluencerIndustryOnlySerializer
from oscarapps.partner.models import PartnerFollow, Partner
from oscarapps.influencers.models import Influencers, Industry
from push_notification.models import APNSDevice
from oscarapps.address.models import TelephoneCode
from oscarapps.partner.models import Category, Style


class LoginView(APIView):
    """
    Api for logging in users.

    DELETE:
    Log the user out by destroying the session.
    Anonymous users will have their cart destroyed as well, because there is
    no way to reach it anymoore

    POST(username, password):
    1. The user will be authenticated. The next steps will only be
       performed is login is succesful. Logging in logged in users results in
       405.
    2. The anonymous cart will be merged with the private cart associated with
       that authenticated user.
    3. A new session will be started, this session identifies the authenticated
       user for the duration of the session, without further need for
       authentication.
    4. The new, merged cart will be associated with this session.
    5. The anonymous session will be terminated.
    6. A response will be issued containing the new session id as a header
       (only when the request contained the session header as well).

    GET (enabled in DEBUG mode only):
    Get the details of the logged in user.
    If more details are needed, use the ``OSCARAPI_USER_FIELDS`` setting to change
    the fields the ``UserSerializer`` will render.
    """
    serializer_class = LoginSerializer

    def get(self, request, format=None):
        if settings.DEBUG:
            if request.user.is_authenticated():
                ser = serializers.UserSerializer(request.user, many=False)
                return Response(ser.data)
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise MethodNotAllowed('GET')

    def merge_baskets(self, anonymous_basket, basket):
        "Hook to enforce rules when merging baskets."
        basket.merge(anonymous_basket)
        anonymous_basket.delete()

    def post(self, request, format=None):
        ser = self.serializer_class(data=request.data)


        if ser.is_valid():

            anonymous_basket = operations.get_anonymous_basket(request)

            user = ser.instance

            # refuse to login logged in users, to avoid attaching sessions to
            # multiple users at the same time.
            if request.user.is_authenticated():
                return Response(
                    {'detail': 'Session is in use, log out first'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED)

            request.user = user

            login_and_upgrade_session(request._request, user)

            # merge anonymous basket with authenticated basket.
            basket = operations.get_user_basket(user)
            if anonymous_basket is not None:
                self.merge_baskets(anonymous_basket, basket)

            operations.store_basket_in_session(basket, request.session)

            return Response("")
        else:
            try:
                email_valid = User.objects.get(email=ser['username'].value,is_influencer=True )
            except:
                data = {"non_field_errors":["Email Error"]}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            return Response(ser.errors, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, format=None):
        """
        Destroy the session.

        for anonymous users that means having their basket destroyed as well,
        because there is no way to reach it otherwise.
        """
        request = request._request
        if request.user.is_anonymous():
            basket = operations.get_anonymous_basket(request)
            if basket:
                operations.flush_and_delete_basket(basket)
        if request.user.is_influencer and request.user.is_authenticated():
            try:
                device = APNSDevice.objects.get(user=request.user)
                device.delete()
            except:
                pass

        request.session.clear()
        request.session.delete()
        request.session = None

        return Response("")


class InfluencerForgotPassword(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        try:
            validate_email(request.data['email'])
        except ValidationError:
            content = {"message": "invalid email"}
            return Response(content, status=status.HTTP_206_PARTIAL_CONTENT)
        try:
            if User.objects.filter(email__exact=request.data["email"], is_influencer=True, is_active=True).exists():
                current_site = Site.objects.get_current()
                domain = current_site.domain
                user = User.objects.get(email__iexact=request.data["email"])
                context = {
                    'domain': domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                tosend = context['protocol'] + '://' + context['domain'] + '/api_v2/reset/' + context['uid'].decode(
                    "utf-8") + '/' + context['token']
                mailid = request.data["email"]
                email = EmailMessage()
                email.subject = "Password Reset at unlabel"
                email.content_subtype = "html"
                email.body = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><META http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
                                    <body>
                                    <br><br>
                                    You're receiving this email because you requested a password reset for your Influencer account in the Unlabel App.
                                    <br><br>
                                    Please go to the following page and choose a new password:
                                    <br><br>
                                    """ + tosend + """
                                    <br><br>
                                    Thanks for using our site!
                                    <br/>
                                    <br/>
                                    <p style='font-size:11px;'><i>*** This is a system generated email; Please do not reply. ***</i></p>
                                    </body>
                                    </head>
                                    </html>"""
                email.from_email = "Unlabel App"
                email.to = [mailid]
                email.send()
                return Response({'code': 'OK'}, status.HTTP_200_OK)
            else:
                content = {'message' : 'We couldnt find your email'}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except:
            return Response({'code': 'Please try again later'}, status=status.HTTP_400_BAD_REQUEST)


class InfluencerFollowedBrands(generics.ListAPIView):
    authentication = authentication.SessionAuthentication
    http_method_names = ('get',)
    pagination_class = pagination.LimitOffsetPagination
    serializer_class = PartnerSerializer

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated() and self.request.user.is_anonymous() == False:
            influencer = self.request.user
            follow_list = PartnerFollow.objects.filter(customer=influencer).values_list('partner', flat=True)
            queryset = Partner.objects.filter(pk__in=follow_list)
            return queryset


class InfluencerProfileUpdate(generics.UpdateAPIView):
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get', 'post')
    serializer_class = InfluencerProfileSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user.is_influencer == True:
                ser = self.serializer_class(request.user, many=False)
                return Response(ser.data)
            else:
                content = {"message": "user is not an influencer."}
                return Response(content, status=status.HTTP_204_NO_CONTENT)
        content = {"message": "user is not authenticated."}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


    def post(self, request, *args, **kwargs):
        contact_number_pattern = re.compile(r'^\+?1?\d{9,15}$')
        name_pattern = re.compile(r'^[A-Za-z. ]+$')

        if request.user.is_authenticated():
            try:
                influencer_user = request.user
            except:
                content = {"message": "Please login and try again"}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            if influencer_user.is_influencer == True:
                if request.data['email']:
                    try:
                        validate_email(request.data['email'])
                        if request.user.email != request.data['email']:
                            email_exists = User.objects.filter(email__iexact=request.data["email"]).count()
                            if email_exists > 0:
                                content = {"message": "The email you entered is already in use."}
                                return Response(content, status=status.HTTP_206_PARTIAL_CONTENT)
                    except ValidationError:
                        content = {"message": "Plesase enter a valid email"}
                        return Response(content, status=status.HTTP_206_PARTIAL_CONTENT)
                    influencer_user.email = request.data['email']

                if request.data["contact_number"] is None or \
                                contact_number_pattern.match(request.data["contact_number"]) is None:
                    content = {"message": "Please enter valid contact number"}
                    return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                else:
                    influencer_user.contact_number = request.data["contact_number"]

                if request.data["first_name"] is None or name_pattern.match(request.data["first_name"]) is None:
                    content = {"message": "Please enter valid first name"}
                    return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                else:
                    influencer_user.first_name = request.data["first_name"]

                if request.data["last_name"] is None or name_pattern.match(request.data["last_name"]) is None:
                    content = {"message": "Please enter valid last name"}
                    return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                else:
                    influencer_user.last_name = request.data["last_name"]

                if request.data['ucc_handle']:
                    influencer_user.ucc_handle = request.data['ucc_handle']
                else:
                    content = {"message": "Please enter valid user name"}
                    return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

                if request.data['telephone_code']:
                    try:
                        tele_code_obj = TelephoneCode.objects.get(id=request.data['telephone_code'])
                    except:
                        tele_code_obj = None
                    influencer_user.telephone_code = tele_code_obj
                else:
                    content = {"message": "Please enter valid telephone code"}
                    return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

                if request.data['gender']:
                    if request.data['gender']== 'M':
                        influencer_user.gender = 'M'
                    elif request.data['gender'] == 'F':
                        influencer_user.gender = 'F'
                    else:
                        content = {"message": "Please enter valid gender"}
                        return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                else:
                    content = {"message": "Please enter valid gender"}
                    return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

                if request.data['image']:
                    influencer_user.image.delete()
                    influencer_user.image = request.data['image']
                else:
                    content = {"message": "Please select an image"}
                    return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

                influencer_user.save();
                content = {"message": "Influencer profile has been successfully updated."}
                return Response(content, status=status.HTTP_200_OK)

            else:
                content = {"message": "user is not an influencer"}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class InfluencerPicAndBio(APIView):
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get', 'post')
    serializer_class = InfluencerPicAndBioSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            try:
                influencer = Influencers.objects.get(users=request.user)
            except:
                influencer = Influencers()
                influencer.users = request.user
                influencer.save()
            ser = self.serializer_class(influencer, many=False)
            return Response(ser.data)
        content = {"message": "user not authenticated"}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            image_ser = self.serializer_class(data=request.data)
            influencer_user = request.user
            try:
                influencer = Influencers.objects.get(users=request.user)
            except:
                content = {"message": "Influencer profile not found."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            if image_ser.is_valid():
                influencer.bio = image_ser.data['bio']
                influencer.save()
                content = {"message": "successfully updated."}
                return Response(content, status=status.HTTP_200_OK)
            else:
                content = {"message": "Please try again."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            content = {"message": "Please login as influencer and try again."}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class PhysicalAttributesUpdate(APIView):
    '''
    View for updating influencer physical attributes
    '''
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get', 'post')
    serializer_class = InfluencerPhysicalAttributesSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            try:
                influencer_profile = Influencers.objects.get(users=request.user)
            except:
                if request.user.is_anonymous() is False:
                    influencer_profile = Influencers()
                    influencer_profile.users = request.user
            attributes_serializer = self.serializer_class(influencer_profile)
            return Response(attributes_serializer.data, status=status.HTTP_200_OK)
        else:
            content = {"message": "Please login as influencer and try again."}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            try:
                influencer_profile = Influencers.objects.get(users=request.user)
            except:
                if request.user.is_anonymous() is False:
                    influencer_profile = Influencers()
                    influencer_profile.users = request.user
            if request.data['waist']:
                influencer_profile.waist = request.data['waist']
            if request.data['hips']:
                influencer_profile.hips = request.data['hips']
            if request.data['chest_or_bust']:
                influencer_profile.chest_or_bust = request.data['chest_or_bust']
            if request.data['height']:
                influencer_profile.height = request.data['height']
            influencer_profile.save()
            content = {"message": "Physical attributes updated successfully."}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        else:
            content = {"message": "Please login as influencer and try again."}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class InfluencerProfileDetails(APIView):
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get',)
    serializer_class = InflencerProfileDetailsSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            try:
                influnencer_profile = Influencers.objects.get(users=request.user)
            except:
                content = {"message": "Please login as influencer and try again"}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            inf_ser = self.serializer_class(influnencer_profile)
            return Response(inf_ser.data)


class InfluencerCurrentLocationView(APIView):
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get', 'post')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            try:
                influencer_profile = Influencers.objects.get(users=request.user)
            except:
                content = {"message": "Please complete the influencer profile information."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            location_serializer = BrandLocationsSerializer(influencer_profile.location, many=False)
            return Response(location_serializer.data)
        else:
            content = {"message": "Please login and try again."}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            try:
                influencer_profile = Influencers.objects.get(users=request.user)
            except:
                content = {"message": "Please complete the influencer profile information."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

            if request.data['location_name'] is None:
                content = {"message": "Please provide location"}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

            else:

                loc = str(request.data['location_name']).split(', ')
                city = ", ".join(str(x) for x in loc[:-2])
                state = str(loc[-2:-1][0])
                if str(loc[-1:][0]) == "United States":
                    country = "USA"
                else:
                    country = str(loc[-1:][0])
                influencer_location = Locations.objects.create(city=city,
                                                        state=state,
                                                        country=country,
                                                        is_influencer_location=True,
                                                        )
                influencer_profile.location = influencer_location
                influencer_profile.save()
                try:
                    Locations.objects.filter(id=request.data['id']).delete()
                except:
                    pass
            # if request.data['country'] is None or request.data['city'] is None:
            #     content = {"message": "Please verify city, state and country."}
            #     return Response(content, status=status.HTTP_206_PARTIAL_CONTENT)
            #
            # influencer_location = Locations()
            # try:
            #     country = Country.objects.get(pk=request.data['country'])
            # except:
            #     content = {"message": "Please verify country id."}
            #     return Response(content, status=status.HTTP_206_PARTIAL_CONTENT)
            # influencer_location.country = country
            # if request.data['state'] and request.data['state'] != "":
            #     try:
            #         state = States.objects.get(pk=request.data['state'])
            #         influencer_location.state = state
            #     except:
            #         content = {"message": "Please verify state id."}
            #         return Response(content, status=status.HTTP_206_PARTIAL_CONTENT)
            #     influencer_location.state = state
            # influencer_location.city = request.data['city']
            # influencer_location.save()
            # influencer_profile.location = influencer_location
            # influencer_profile.save()
            content = {"message": "successfully updated location."}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {"message": "Please login as influencer and try again."}
            return Response(content, status=status.HTTP_206_PARTIAL_CONTENT)


#
class InfluencerChangePassword(APIView):
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get', 'post')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            if 'old_password' in request.data and 'new_password' in request.data:
                if not self.request.user.check_password(request.data['old_password']):
                    content = {"message": "The current password is wrong"}
                    return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                else:
                    influencer = request.user
                    influencer.set_password(request.data['new_password'])
                    influencer.save()
                    update_session_auth_hash(request, influencer)
                    content = {"message": "Password updated successfully."}
                    return Response(content, status=status.HTTP_200_OK)
            else:
                content = {"message": "Password not found."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            content = {"message": "Please login as influencer and try again."}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class InfluencerContentsLink(APIView):
    def get(self, request, *args, **kwargs):
        privacy_policy_url = "www.google.com"
        terms_conditions_url = "www.google.com"
        operations_agreement_url = "www.google.com"
        content = {'privacy_policy_url': privacy_policy_url,
                   'terms_conditions_url': terms_conditions_url,
                   'operations_agreement_url': operations_agreement_url
        }
        return Response(content, status=status.HTTP_200_OK)


class InfluencerGetBalance(APIView):
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            influencer_remaining = 999
            content = {'results': {'balance': influencer_remaining}}
            return Response(content, status=status.HTTP_200_OK)


class InfluencerUniqueUcc(APIView):
    """
    Check the ucc handle for a unique value
    """

    def get(self, request, *args, **kwargs):
        if User.objects.filter(ucc_handle=request.GET.get('ucc_handle')).exists() or not request.GET.get('ucc_handle'):
            content = {'message': 'Already exist'}
            return Response(content, status=status.HTTP_409_CONFLICT)
        else:
            content = {'message': 'success'}
            return Response(content, status=status.HTTP_200_OK)


class InfluencerProfileStyles(APIView):
    """
    To store the influencer's style
    """
    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get', 'post')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            try:
                influencer = Influencers.objects.get(users=request.user)
            except:
                influencer = Influencers()
                influencer.users = request.user
                influencer.save()
            ser = InfluencerStyleSerializer(influencer, many=False)
            return Response(ser.data)
        content = {"message": "user not authenticated"}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            styles_data = InfluencerPostStyleSerializer(data=request.data)
            try:
                influencer = Influencers.objects.get(users=request.user)
            except:
                content = {"message": "Influencer profile not found."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            if styles_data.is_valid():
                influencer.styles = styles_data.data['styles']
                influencer.save()
                content = {"message": "successfully updated."}
                return Response(content, status=status.HTTP_200_OK)
            else:
                content = {"message": "Please try again."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            content = {"message": "Please login as influencer and try again."}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

class InfluencerProfileListing(generics.ListAPIView):
    pagination_class = InfluencerListPagination
    permissions = permissions.AllowAny
    authentication=None
    serializer_class = InflencerProfileDetailsSerializer
    http_method_names = ('get',)

    # ZA - sort by a to z
    # AZ - sort by z to a
    # ASC - sort by date ascending
    # DESC - sort by date descending

    def get_queryset(self, *args, **kwargs):
        style_selected = self.request.GET.get('style',None)
        location_selected = self.request.GET.get('location',None)
        gender_selected = self.request.GET.get('gender',None)
        order = self.request.GET.get('order')

        influencers_list = Influencers.objects.all()

        if gender_selected:
            gender_selected = gender_selected.split(',')
            influencers_list = influencers_list.filter(users__gender__in=gender_selected)
        if style_selected:
            style_selected = style_selected.split(',')
            styles = Style.objects.filter(id__in=style_selected)
            influencers_list = influencers_list.filter(styles__in=styles)
        if location_selected:
            location_selected = location_selected.split(',')
            location_citys = Locations.objects.filter(id__in=location_selected).values_list('city',flat=True)
            locations = Locations.objects.filter(city__in=location_citys)
            influencers_list = influencers_list.filter(location__in=locations)

        if order:
            if order == 'ZA':
                influencers_list = influencers_list.order_by('users.first_name')
            elif order == 'AZ':
                influencers_list = influencers_list.order_by('-users.first_name')
            elif order == 'ASC':
                influencers_list = influencers_list.order_by('-created')
            elif order == 'DESC':
                influencers_list = influencers_list.order_by('created')

        return influencers_list


class InfluencerIndustryListView(generics.ListAPIView):
    http_method_names = ('get',)
    pagination_class = None
    queryset = Industry.objects.all()
    serializer_class = InfluencerIndustrySerializer


class InfluencerIndustryUpdateView(APIView):

    authentication = authentication.SessionAuthentication
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get', 'post')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            try:
                influencer = Influencers.objects.get(users=request.user)
            except:
                influencer = Influencers()
                influencer.users = request.user
                influencer.save()
            ser = InfluencerIndustryOnlySerializer(influencer, many=False)
            return Response(ser.data)
        content = {"message": "user not authenticated"}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

    def post(self,request,*args,**kwargs):
        if request.user.is_authenticated() and request.user.is_influencer is True:
            try:
                influencer = Influencers.objects.get(users=request.user)
            except:
                content = {"message": "Influencer profile not found."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            industry_data = InfluencerIndustryOnlySerializer(data=request.data)
            if industry_data.is_valid():
                influencer.industry = industry_data.data['industry']
                influencer.save()
                content = {"message": "successfully updated."}
                return Response(content, status=status.HTTP_200_OK)
            else:
                content = {"message": "Please try again."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            content = {"message": "Please login as influencer and try again."}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class InfluencerProfileAnalyticsView(APIView):
    '''
    View for retrieving
    '''
    http_method_names = ('get',)
    pagination_class = None

    def get(self,request,*args,**kwargs):
        data = {
                'completed_rentals':99,
                'rental_desc':"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum "
                              "has been the industry's standard dummy text ever since the 1500s, when an unknown "
                              "printer took a galley of type and scrambled it to make a type specimen book.",
                'total_earnings':99,
                'earning_desc':"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum "
                              "has been the industry's standard dummy text ever since the 1500s, when an unknown "
                              "printer took a galley of type and scrambled it to make a type specimen book.",
                'engagement':99,
                'engagement_desc':"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum "
                              "has been the industry's standard dummy text ever since the 1500s, when an unknown "
                              "printer took a galley of type and scrambled it to make a type specimen book.",
        }
        return Response(data, status=status.HTTP_200_OK)



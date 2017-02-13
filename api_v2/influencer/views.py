from __future__ import unicode_literals

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from rest_framework import permissions, authentication
from django.core.mail.message import EmailMessage
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes
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

from api_v2.catalogue.serializers import PartnerSerializer
from users.models import User
from .serializers import LoginSerializer, InfluencerProfileSerializer
from oscarapps.partner.models import PartnerFollow, Partner
from oscarapps.influencers.models import Influencers


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
            if User.objects.filter(email__iexact=request.data["email"],is_influencer=True,is_active=True).exists():
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
                content = {'message : Not a valid Influencer email.'}
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

class InfluencerProfileUpdate(ModelViewSet):
    # authentication = authentication.SessionAuthentication
    # permission_classes = (permissions.IsAuthenticated,)
    # http_method_names = ('get','post')
    # serializer_class = InfluencerProfileSerializer
    model = User

    # def get(self,request,*args,**kwargs):
    #     if request.user.is_authenticated():
    #         ser = self.serializer_class(request.user, many=False)
    #         return Response(ser.data)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    #
    # def post(self,request,*args,**kwargs):
    #     if request.user.is_authenticated():
    #         try:
    #             influencer_user = request.user
    #         except :
    #             content = {"message": "Please login and try again"}
    #             return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    #         if request.data['email']:
    #             try:
    #                 validate_email(request.data['email'])
    #             except ValidationError:
    #                 content = {"message": "invalid email"}
    #                 return Response(content, status=status.HTTP_206_PARTIAL_CONTENT)
    #             influencer_user.email = request.data['email']
    #         if request.data['contact_number']:
    #              contact_number_pattern = re.compile(r'^\+?1?\d{9,15}$')
    #             if contact_number is not None and contact_number_pattern.match(contact_number) is None:



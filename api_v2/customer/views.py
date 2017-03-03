from __future__ import unicode_literals

import re

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail.message import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_auth.registration.views import SocialLoginView
from rest_framework import permissions, authentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v2.utils import *
from .serializers import CustomerRegisterSerializer
from push_notification.models import Device, APNSDevice, SNS


# ######################################push testing

# class PushNotificationView(APIView):
#     """
#         View for Push notifications
#     """
#
#     def get(self, request, *args, **kwargs):
#         app = Application.objects.create(name='tester_application10')
#
#         apns_platform = Platform.objects.create(
#             platform='APNS_SANDBOX',
#             application=app,
#             arn="arn:aws:sns:ap-south-1:275431664439:app/APNS_SANDBOX/unlabel_-7"
#         )
#
#         apple_device = Device.objects.create(device_id="ec04b7235df4a21183f062f51ffa2b975c1eb82e",
#                                              push_token="9F74C3B1E23CF6DAFD0ECC77D2BAFA4B620F75D13B1A98F89ED8C3F9A147A2B2",
#                                              platform=apns_platform
#         )
#
#         apple_device.register()
#
#         topic = Topic.objects.create(
#             name='test_topic',
#             application=app,
#         )
#
#         topic.register()
#         #topic.register_device(arn_device)
#
#         message = PushMessage(
#             badge_count=1,
#             context='url_alert',
#             context_id='none',
#             has_new_content=True,
#             message="Unlabel Welcomes you",
#             sound="default"
#         )
#         apple_device.send(message)
#
#         return Response({'message': "successfully pushed"})


#######################################push testing ends


# class DjangoPush(APIView):
#     def post(self,request,*args,**kwargs):
#
#         # dev_id = request.data['device_id']
#         # p_token = request.data['token']
#         dev_id = "F629D32A665D546A6C7EF9A535C340404B8DD27DB9541E08A1F71570FE8590D0"
#         if re.match("[0-9a-fA-F]{64}", "F629D32A665D546A6C7EF9A535C340404B8DD27DB9541E08A1F71570FE8590D0") is not None:
#             device, created = APNSDevice.objects.get_or_create(user=request.user)
#             device.registration_id = "F629D32A665D546A6C7EF9A535C340404B8DD27DB9541E08A1F71570FE8590D0"
#             device.active = True
#             device.save()
#             if created:
#                 device.send_message("This is the bloody push notification.")
#                 return Response({'message':"done"},status=status.HTTP_201_CREATED)
#             else:
#                 return Response()
#         else:
#             return Response("device_token invalid or not provided", status=status.HTTP_400_BAD_REQUEST)




class RegisterDevice(APIView):
    """
    API view to register an Android/IOS device.
    """
    authentication = (authentication.SessionAuthentication,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        response = Response(data={"status": False})
        device_type = request.data.get('device_type', '').lower()
        print("-------------------",device_type)
        if request.user.is_authenticated() and request.user.is_influencer:
            if device_type == 'ios':
                ua = request.data.get('device', '').lower()
                token_updated = False
                # Device.objects.create(user=request.user)
                reg_status = self.registration_checking(ua, request)
                return reg_status
        return Response({'status': 'HTTP_404_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

    def registration_checking(self, ua, request):
        deviceID = request.data.get('udid')
        registrationID = request.data.get('push_token')
        if not deviceID or not registrationID:
            return Response({'message': "missing attributes"}, status=status.HTTP_206_PARTIAL_CONTENT)
        device, created = APNSDevice.objects.get_or_create(device_id=deviceID)
        if request.user.is_authenticated():
            device.user = request.user
        else:
            device.user = None
        if not device.registration_id:
            device.registration_id = registrationID
            device.save()
        if not device.registration_id == registrationID and not created:
            if device.aws_subscription_arn:
                self.update_sns_endpoint(device.aws_subscription_arn, registrationID, device)
                device.registration_id = registrationID
                device.save()
        if not device.aws_subscription_arn:
            self.create_sns_endpoint(registrationID, device)
        device.save()

        return Response({'status': 'HTTP_200_OK'}, status=status.HTTP_200_OK)

    def create_sns_endpoint(self, token, device):
        sns = SNS()
        response = sns.create_gcm_endpoint(token=token)
        data = response
        device.aws_subscription_arn = data.get('EndpointArn')
        device.save()
        return True

    def update_sns_endpoint(self, old_arn, new_token, device):
        sns = SNS()
        response = sns.delete_gcm_endpoint(arn=old_arn)
        self.create_sns_endpoint(token=new_token, device=device)
        return True


class SendNotification(APIView):
    """
    View to send notifications
    """

    def dispatch(self, *args, **kwargs):
        return super(SendNotification, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        payload_dict = ''
        # notification_id = self.request.POST.get('notif_id')
        # selected_ids = self.request.POST.get('nofication_ids')
        # new_push_text = GeneralPushNotification.objects.get(id=notification_id)
        # if selected_ids:
        #     selected_ids = selected_ids.split(',')
        # device_ids = NotificationLog.objects.filter(id__in=selected_ids, sent_status='DRAFT').values_list('device_id',
        #                                                                                                   flat=True)
        devices = APNSDevice.objects.filter(device_id__in=['353E3132835144E5876AE5E4D6BE76DD'])
        print(">>>>>>>>>>>>devices", devices)
        for device in devices:
            deviceid = device.device_id
            registrationid = device.registration_id
            arn = device.aws_subscription_arn
            image = ''
            msg = "payload test from aws snsssss"
            payload_dict = {"aps": {"alert": "test", "sound": "default", "badge": 0}, "uri": "www.google.com"}

            s = SNS()
            try:
                response = s.send_message(arn, msg, payload_dict)
                print("-----------------------response from aws sns======>> ", response)
                if response.get("MessageId"):
                    # current_notif = NotificationLog.objects.get(device_id=deviceid, notification_id=notification_id)
                    # current_notif.send_count = 1
                    # current_notif.sent_status = 'SEND'
                    # current_notif.notif_time = datetime.now()
                    # current_notif.save()
                    # if new_push_text.notif_type == 'OFFER':
                    #     offer_notif = OfferLog.objects.get(device_id=deviceid, notification_id=notification_id)
                    #     offer_notif.send_count = 1
                    #     offer_notif.sent_status = 'SEND'
                    #     offer_notif.offer_sent_time = datetime.now()
                    #     offer_notif.save()
                    return Response({'message': 'double success'})
            except Exception as e:
                print("<<<<<<<<<<<<<<<<<<<Exception--> ", e)
        return Response({'success': 1})


class CustomerRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        try:
            if len(str(request.data["first_name"])) != 0 and len(str(request.data["first_name"])) < 30:
                match = re.search('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                  request.data["email"])
                if match:
                    # email_exist = User.objects.filter(email=request.data["email"])
                    email_exist = User.objects.filter(email__iexact=request.data["email"])
                    if not email_exist:
                        serializer = CustomerRegisterSerializer(data=request.data)
                        if serializer.is_valid():
                            serializer.save()

                            mailid = request.data["email"]
                            email = EmailMessage()
                            email.subject = "Registration succesful at unlabel"
                            email.content_subtype = "html"
                            email.body = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><META http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
                                            <body>
                                            <h2>Welcome to unlabel</h2>
                                            <p style = 'font-size:14px;'>Hello,</p>
                                            <p>Your email has been succesfully registered with Unlabel.<br/>
                                            </p>
                                            <br/>
                                            <br/>
                                            Thank you!<br/><br/>
                                            <p style='font-size:11px;'><i>*** This is a system generated email; Please do not reply. ***</i></p>
                                            </body>
                                            </head>
                                            </html>"""
                            email.from_email = "Unlabel App"
                            email.to = [mailid]
                            email.send()
                            newUser = User.objects.get(email=request.data["email"])
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        content = {"message": "email already registered"}
                        return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                else:
                    content = {"invalid email"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {"invalid name. name should be less than 30 characters"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {"message": "Please validate the data and try again."}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class CustomerPasswordUpdateView(APIView):
    authentication = (authentication.SessionAuthentication,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated():
                customer = request.user
            # customer=User.objects.get(email=request.data["email"])
            else:
                content = {"message": "Please login first."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            customer.set_password(request.data["password"])
            customer.save()
            content = {"message": "password changed successfully. Please login to continue."}
            request.session.clear()
            request.session.delete()
            request.session = None
            return Response(content, status=status.HTTP_201_CREATED)
        except:
            content = {"message": "given email does not exist."}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class CustomerForgotPassword(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        # if request.data["email"]:
        try:
            if User.objects.filter(email__iexact=request.data["email"]).exists():
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
                try:
                    tosend = context['protocol'] + '://' + context['domain'] + '/api_v2/reset/' + context['uid'].decode(
                        "utf-8") + '/' + context['token']
                    mailid = request.data["email"]
                    email = EmailMessage()
                    email.subject = "Password Reset at unlabel"
                    email.content_subtype = "html"
                    email.body = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><META http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
                                        <body>
                                        <br><br>
                                        You're receiving this email because you requested a password reset for your user account at Unlabel.
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
                except:
                    return Response({'code': 'Please try again later'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {"message": "email does not exist"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class CustomerProfileUpdateView(APIView):
    authentication = (authentication.SessionAuthentication,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated():
                customer = request.user
            # customer = User.objects.get(email = request.data["email"])
            else:
                content = {"message": "Please login first."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except:
            content = {"message": "given email not authenticated."}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        customer.first_name = request.data["first_name"]
        customer.save()
        content = {"message": "name changed successfully"}
        return Response(content, status=status.HTTP_200_OK)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class CustomerProfileDeleteView(APIView):
    authentication = authentication.SessionAuthentication
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated():
                customer = request.user
            else:
                content = {"message": "Please login first."}
                return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except:
            content = {"message": "given email not authenticated."}
            return Response(content, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        customer.is_active = False
        customer.save()
        content = {"message": "Account deleted Successfully"}
        return Response(content, status=status.HTTP_200_OK)


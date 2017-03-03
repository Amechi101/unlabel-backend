from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# from scarface.models import Application, Platform, Device, Topic, PushMessage
from unlabel import base_settings
from django.utils.translation import ugettext_lazy as _
from unlabel import settings
from django.db.models.signals import post_delete
import json
import boto3


class SNS(object):
    def __init__(self):
        self.client = boto3.client('sns', aws_access_key_id=base_settings.AWS_SNS_ACCESS_KEY_ID,
                                   aws_secret_access_key=base_settings.AWS_SNS_SECRET_ACCESS_KEY,
                                   region_name=base_settings.AWS_DEFAULT_REGION, )
        self.platform_arn = base_settings.AWS_SNS_PLATFORM_APP_ARN

    def create_gcm_endpoint(self, token):
        response = self.client.create_platform_endpoint(PlatformApplicationArn=self.platform_arn,Token=token,
                                                        Attributes={'Enabled': 'true'})
        return response

    def delete_gcm_endpoint(self, arn):
        response = self.client.delete_endpoint(
            EndpointArn=arn
        )
        return response

    def send_message(self, arn, message, payload_dict=None):
        data_dict = {'message': message}
        if payload_dict:
            data_dict.update(payload_dict)
        apns_dict = {'data': data_dict}
        apns_string = json.dumps(apns_dict, ensure_ascii=False)
        message = {'default': message, 'GCM': apns_string}
        messageJSON = json.dumps(message, ensure_ascii=False)
        response = self.client.publish(
            TargetArn=arn,
            MessageStructure='json',
            Message=messageJSON
        )
        return response


@python_2_unicode_compatible
class Device(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"), blank=True, null=True)
    active = models.BooleanField(verbose_name=_("Is active"), default=True,
                                 help_text=_("Inactive devices will not be sent notifications"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name or \
               str(self.device_id or "") or \
               "%s for %s" % (self.__class__.__name__, self.user or "unknown user")


class APNSDevice(Device):
    device_id = models.TextField(verbose_name=_("Device ID"), blank=True, null=True, db_index=True,
                                 help_text="UDID / UIDevice.identifierForVendor()")
    registration_id = models.CharField(verbose_name=_("Registration ID"), max_length=200, unique=True)
    aws_subscription_arn = models.TextField(verbose_name=_("APNSDevice_AWS_Topic_Subscription_ARN"), blank=True,
                                           null=True)

    class Meta:
        verbose_name = _("APNS device")


def delete_aws_sns(sender, instance, **kwargs):
   if instance.aws_subscription_arn:
       sns = SNS()
       response = sns.delete_gcm_endpoint(arn=instance.aws_subscription_arn)
   return True


post_delete.connect(delete_aws_sns, sender=APNSDevice)


# class NotificationType(models.Model):
#     product_rented = 'product_rented'
#     product_reservation_lost = 'product_reservation_lost'
#     product_not_live = 'product_not_live'
#     live_not_returned = 'live_not_returned'
#     followed_brand_product_added = 'followed_brand_product_added'
#     new_brand_added = 'new_brand_added'
#     general_notificatin = 'general_notification'
#
#     type_choice = (
#         (product_rented, 'Producted Rented'),
#         (product_reservation_lost, 'Product Reservation Lost'),
#         (product_not_live, 'Product Not Live'),
#         (live_not_returned,'Live And Not Returned')
#         (followed_brand_product_added,'Followed Brand Added Product')
#         (new_brand_added,'New Brand Added')
#         (general_notificatin,'General Notification')
#
#
#     )
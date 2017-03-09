import json
import sys
from optparse import make_option
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from oscarapps.catalogue.models import Product
from oscarapps.influencers.models import Influencers, InfluencerProductReserve, InfluencerProductUnreserve
from push_notification.models import APNSDevice,NotificationDetails, SNS
from users.models import User

from oscar.core.loading import get_model


class Command(BaseCommand):
    '''
    Job to send notification to
    influencer to remind about
    product rental.

    TO BE EXECUTED EVERY DAY

    '''
    help = "Influencers will receive notification when a product is rented."

    def handle(self, *args, **options):
        notifications = NotificationDetails.objects.filter(notification_type='pr',sent=False)
        for notification in notifications:
            device = APNSDevice.objects.get(user=notification.user)
            deviceid = device.device_id
            registrationid = device.registration_id
            arn = device.aws_subscription_arn
            msg = notification.text
            payload_dict = json.loads(notification.payload)

            s = SNS()
            try:
                response = s.send_message(arn, msg, payload_dict)
                if response.get("MessageId"):
                    notification.sent=True
                    notification.date_sent=datetime.now()
                    notification.save()
            except Exception as e:
                print("--> Exception in sending push notification(prl)-->", e)
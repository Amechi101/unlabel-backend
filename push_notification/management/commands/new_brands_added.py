import json
import sys
from optparse import make_option
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from oscarapps.catalogue.models import Product
from oscarapps.partner.models import Partner
from oscarapps.influencers.models import Influencers, InfluencerProductReserve, InfluencerProductUnreserve
from push_notification.models import APNSDevice,NotificationDetails, SNS
from users.models import User

from oscar.core.loading import get_model


class Command(BaseCommand):
    '''
    Job to notify all influencers about
    new brands added to unlabel

    To be executed every hour
    '''
    help = "To notify all influencers about the addition of new brands to unlabel"

    def handle(self, *args, **options):
        #Selecting new brands
        new_partners = Partner.objects.filter(created__lt=datetime.now()-timedelta(hours=1))
        partner_names=""
        for partner in new_partners:
            partner_names = partner_names + ", " + partner.name

        influencers = Influencers.objects.all()
        for influencer in influencers:
            notification = NotificationDetails()
            notification.notification_type = 'nba'
            notification.sent = False
            notification.text="New brands have been added to unlabel. Check "+partner_names[:-1]
            notification.payload=json.dumps({'type':'nba'})
            notification.user = influencer.users
            notification.save()

        #Sending notification to each influencer
        notifications = NotificationDetails.objects.filter(notification_type='nba',sent=False)
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



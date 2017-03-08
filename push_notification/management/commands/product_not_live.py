import json
import sys
from optparse import make_option
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from oscarapps.catalogue.models import Product
from oscarapps.influencers.models import Influencers, InfluencerProductReserve, InfluencerProductUnreserve
from push_notification.models import APNSDevice, NotificationDetails, SNS
from users.models import User

from oscar.core.loading import get_model


class Command(BaseCommand):
    '''
    Job to send notification to
    influencer to remind about
    making the product live.

    TO BE EXECUTED EVERY DAY

    '''
    help = "Influencers will receive notification if product is not live after 4 days."

    def handle(self, *args, **options):
        products_reserved = InfluencerProductReserve.objects.filter(
            date_rented__lt=datetime.today() - timedelta(days=4))
        for product_reserved in products_reserved:
            try:
                product = Product.objects.get(pk=product_reserved.product)
                if product.rental_status == 'REN' and product.status == 'R':
                    product_name = ""
                    if product.structure == 'child':
                        product_name = product.parent.title
                    else:
                        product_name = product.title
                    influencer = Influencers.objects.get(pk=product_reserved.influencer)
                    notification = NotificationDetails()
                    notification.notification_type = 'pnl'
                    notification.sent = False
                    notification.text = "A Product you have rented is not live yet. Please check "+product_name+" on Unlabel."
                    notification.user = influencer.users
                    notification.payload=json.dumps({'type':'pnl','product_id':product.pk})
                    notification.save()
            except Exception as e:
                print("------------> Exception in product_not_live--> ", e)

        #Sending notification to influeners
        notifications = NotificationDetails.objects.filter(notification_type='pnl',sent=False)
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
                print("--> Exception in sending push notification(pnl)-->", e)



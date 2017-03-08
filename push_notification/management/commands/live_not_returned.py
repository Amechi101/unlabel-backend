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
    influencer to remind return
    of the live product

    TO BE EXECUTED EVERY DAY

    '''
    help = "Influencers will receive notification if a live product is not returned after 24hrs"

    def handle(self, *args, **options):
        #Selecting products to unreserve and drafting notification to send
        products_reserved = InfluencerProductReserve.objects.filter(date_live__lt=datetime.today()-timedelta(days=1))
        for product_reserved in products_reserved:
            try:
                product=Product.objects.get(pk=product_reserved.product)
                if product.rental_status=='REN' and product.status=='L':
                    product_name=""
                    if product.structure=='child':
                        product_name=product.parent.title
                    else:
                        product_name = product.title
                    influencer=Influencers.objects.get(pk=product_reserved.influencer)
                    notification = NotificationDetails()
                    notification.notification_type = 'lnr'
                    notification.sent = False
                    notification.text="You have not returned the product " + str(product_name)+"."
                    notification.payload=json.dumps({'type':'lnr','product_id':product.pk})
                    notification.user = influencer.users
                    notification.save()
            except Exception as e:
                print("------------> Exception in live_not_returned--> ",e)

        #Sending notification to influeners
        notifications = NotificationDetails.objects.filter(notification_type='lnr',sent=False)
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
                print("--> Exception in sending push notification (lnr)-->", e)




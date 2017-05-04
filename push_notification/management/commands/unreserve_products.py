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
    Job to unreserve products and
    send notification to influencer
    regarding the loss of reservation.

    TO BE EXECUTED EVERY DAY

    '''
    help = "Products which are not rented after 4 days from the date of reservation will be unreserved"

    def handle(self, *args, **options):
        #Selecting products to unreserve and drafting notification to send
        products_reserved = InfluencerProductReserve.objects.filter(date_rented=None,
                                                                    date_reserved__lt=datetime.today() - timedelta(
                                                                        days=3))
        for product_reserved in products_reserved:
            try:
                influencer = Influencers.objects.get(pk=product_reserved.influencer)
                product = Product.objects.get(pk=product_reserved.product)
                product_unreserved = InfluencerProductUnreserve()
                product_unreserved.influencer = influencer
                product_unreserved.product = product
                product_unreserved.type = 'SYS'
                product.status = "U"
                name = product.title
                if product.structure == "child":
                    base_product = Product.objects.get(pk=product.parent.id)
                    base_product.rental_status = 'U'
                    base_product.save()
                    name = base_product.title
                product.save()
                product_unreserved.save()
                notification = NotificationDetails()
                notification.notification_type = 'prl'
                notification.sent = False
                notification.text="You have lost your reservation for "+ str(name) + ""
                notification.user = influencer.users
                notification.payload=json.dumps({'type':'prl','product_id':product.pk})
                notification.save()
                product_reserved.delete()
            except:
                print("---> Error in unreservation job ---> ",product)

        # Sending the drafted notification to the devices
        notifications = NotificationDetails.objects.filter(notification_type='prl',sent=False)
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



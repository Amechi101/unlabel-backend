import json
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.core.mail.message import EmailMessage
from oscar.apps.partner.models import StockRecord
from oscarapps.catalogue.models import Product
from oscarapps.influencers.models import Influencers, InfluencerProductReserve, InfluencerProductUnreserve
from push_notification.models import APNSDevice, NotificationDetails, SNS


class Command(BaseCommand):
    """
    Job to unreserve products and
    send notification to influencer
    regarding the loss of reservation.

    TO BE EXECUTED EVERY DAY
    """
    help = "Products which are not rented after 4 days from the date of reservation will be unreserved"

    def handle(self, *args, **options):
        """
        Selecting products to unreserve and drafting notification to send
        """
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
                # Email notification when product is Unreserved
                self.send_email_for_unreserved_product(product_unreserved, influencer.users)
                notification = NotificationDetails()
                notification.notification_type = 'prl'
                notification.sent = False
                notification.text = "You have lost your reservation for "+ str(name) + ""
                notification.user = influencer.users
                notification.payload = json.dumps({'type': 'prl','product_id': product.pk})
                notification.save()
                product_reserved.delete()
            except:
                print("---> Error in unreservation job ---> ",product)

        # Sending the drafted notification to the devices
        notifications = NotificationDetails.objects.filter(notification_type='prl',sent=False)
        for notification in notifications:
            device = APNSDevice.objects.get(user=notification.user)
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

    def send_email_for_unreserved_product(self, product_to_live, influencer_user):
        """
            Send email when product is Unreserved
        """
        stock_brand = StockRecord.objects.filter(product=product_to_live)[0].partner  # partner name
        brand_user = stock_brand.users.all()[0]  # partner's mail id
        self.mail_send(brand_user)  # send mail to partner
        self.mail_send(influencer_user.users)  # send mail to influencer

    def mail_send(self, to_mail):
        """
            Send mail to a recipient
        """
        mailid = to_mail
        email = EmailMessage()
        email.subject = "Product Unreserved"
        email.content_subtype = "html"
        email.body = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><META http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
                        <body>
                        <h2>Welcome to unlabel</h2>
                        <p style = 'font-size:14px;'>Hello,</p>
                        <p>Product has been unreserved.<br/>
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



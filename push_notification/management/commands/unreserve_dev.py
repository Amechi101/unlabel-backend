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
        products_reserved = InfluencerProductReserve.objects.all()
        for products in products_reserved:
            products.delete()

        products = Product.objects.all()
        for product in products:
            product.status = 'D'
            product.rental_status = 'U'
            product.influencer=None
            product.save()


        print("---Done---")


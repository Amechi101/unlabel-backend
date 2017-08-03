import json
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from oscarapps.catalogue.models import Product
from oscarapps.influencers.models import Influencers, InfluencerProductReserve
from push_notification.models import APNSDevice, NotificationDetails, SNS


class Command(BaseCommand):
    """
    Job to send notification to
    influencer to remind return
    of the live product

    TO BE EXECUTED EVERY DAY
    """
    help = "Influencers will receive notification if a live product is not returned after 24hrs"

    def handle(self, *args, **options):
        influencer_products = InfluencerProductReserve.objects.all()
        for influencer_product in influencer_products:
            product = Product.objects.get(id=influencer_product.product.id)
            influencer = Influencers.objects.get(id=influencer_product.influencer.id)
            if product.structure == 'child':
                original_product = product.parent
            else:
                original_product = product

            original_product.influencer = influencer
            original_product.save()


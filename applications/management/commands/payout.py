# -*- coding: utf-8 -*-
import sys
from optparse import make_option
import stripe
from django.core.management.base import BaseCommand, CommandError

from unlabel import base_settings
from oscar.core.loading import get_model

Influencer = get_model('influencers', 'Influencers')
InfluencerPayout = get_model('payment', 'InfluencerPayout')
InfluencerCommission = get_model('payment', 'InfluencerCommission')
BrandCommission = get_model('payment', 'BrandCommission')
Brand = get_model('partner', 'Partner')
BrandPayout = get_model('payment', 'BrandPayout')
StripeCredential = get_model('payment', 'StripeCredential')

stripe.api_key = base_settings.STRIPE_API_KEY


class Command(BaseCommand):
    help = "Populates the list of countries with data from pycountry."

    def add_arguments(self, parser):
        parser.add_argument('start_date', help='Start Date')
        parser.add_argument('end_date', help='End date')

    def handle(self, *args, **options):

        start_date, end_date = options['start_date'], options['end_date']
        influencer_list = []
        influencer_commissions = InfluencerCommission.objects.filter(created__range=[start_date, end_date])
        for obj in influencer_commissions:
            obj.is_completed = True
            obj.save()
            influencer_list.append(obj.influencer)
        influencer_list = list(set(influencer_list))
        for influencer in influencer_list:
            total_influencers = influencer_commissions.filter(influencer=influencer)
            total_commission = 0
            for obj in total_influencers:
                total_commission += obj.amount
            InfluencerPayout.objects.create(stripe_credential=StripeCredential.objects.get(user=influencer.users),
                                            total_amount=total_commission)
        brand_list = []
        brand_commissions = BrandCommission.objects.filter(created__range=[start_date, end_date])
        for obj in brand_commissions:
            obj.is_completed = True
            obj.save()
            brand_list.append(obj.brand)
        brand_list = list(set(brand_list))
        for brand in brand_list:
            total_brands = brand_commissions.filter(brand=brand)
            total_commission = 0
            for obj in total_brands:
                total_commission +=obj.amount
            BrandPayout.objects.create(stripe_credential=StripeCredential.objects.get(user=brand.users.all().first()),
                                total_amount=total_commission)

        for transaction in BrandPayout.objects.all():
             try:
                transfer = stripe.Transfer.create(
                  amount=round(((int(transaction.total_amount))*100), 2),
                  currency="usd",
                  destination=transaction.stripe_credential.stripe_id,
                  transfer_group=transaction.stripe_credential.user.email,
                )
                try:
                    if transfer["status"] == "paid":
                        transaction.is_completed = True
                        transaction.reference = str(transfer["id"])
                        transaction.save()
                except:

                    if transfer["status"] == "paid":
                        trn = stripe.Transfer.retrieve(transfer["id"])
                        trn.reversals.create()
             except:

                 pass

        for transaction in InfluencerPayout.objects.all():
            try:
                transfer = stripe.Transfer.create(
                  amount=round(((int(transaction.total_amount))*100), 2),
                  currency="usd",
                  destination=transaction.stripe_credential.stripe_id,
                  transfer_group=transaction.stripe_credential.user.email,
                )
                try:
                    if transfer["status"] == "paid":
                        transaction.is_completed = True
                        transaction.reference = str(transfer["id"])
                        transaction.save()
                except:
                    if transfer["status"] == "paid":
                        trn = stripe.Transfer.retrieve(transfer["id"])
                        trn.reversals.create()
            except:

                 pass
        print("success")






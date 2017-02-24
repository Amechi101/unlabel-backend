from oscar.apps.payment.models import *
from django.db import models
from django.core.exceptions import ValidationError

from oscar.apps.order.models import Order
from oscarapps.partner.models import Partner
from oscarapps.influencers.models import Influencers


class BaseApplicationModel(models.Model):
    """
    An abstract base class model that common attributes
    """
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'payment'
        abstract = True


class InfluencerCommission(BaseApplicationModel):
    influencer = models.ForeignKey(Influencers, blank=True, null=True, verbose_name="Influencer")
    order = models.ForeignKey(Order, blank=True, null=True, verbose_name="Order")
    amount = models.DecimalField(max_digits=5, decimal_places=2,
                                verbose_name="Commission received")

    def __str__(self):
        return str(self.influencer)+", "+str(self.order)+", "+str(self.amount)


class BrandCommission(BaseApplicationModel):
    brand = models.ForeignKey(Partner, blank=True, null=True, verbose_name="Brand")
    order = models.ForeignKey(Order, blank=True, null=True, verbose_name="Order")
    amount = models.DecimalField(max_digits=5, decimal_places=2,
                                verbose_name="Commission received")

    def __str__(self):
        return str(self.brand)+", "+str(self.order)+", "+str(self.amount)


class UnlabelCommission(BaseApplicationModel):
    order = models.ForeignKey(Order, blank=True, null=True, verbose_name="Order")
    amount = models.DecimalField(max_digits=5, decimal_places=2,
                                verbose_name="Commission received")

    def __str__(self):
        return str(self.order)+", "+str(self.amount)


class CommissionConfiguration(BaseApplicationModel):
    influencer_commission = models.DecimalField(max_digits=5, decimal_places=2,
                                                verbose_name="Influencer commission percentage")
    brand_commission = models.DecimalField(max_digits=5, decimal_places=2,
                                                verbose_name="Brand commission percentage")
    unlabel_commission = models.DecimalField(max_digits=5, decimal_places=2,
                                                verbose_name="Unlabel commission percentage")

    def clean(self):
         if float(self.brand_commission+self.influencer_commission+self.unlabel_commission) != float(100):
             raise ValidationError('Total sum of commissions should be 100')

    def __str__(self):
        return_string = "BC: "+str(self.brand_commission)+", IC:" + str(self.influencer_commission)+", UC:"+str(self.unlabel_commission)
        return return_string



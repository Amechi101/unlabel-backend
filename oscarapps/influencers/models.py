# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string
from decimal import Decimal
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models.signals import pre_save

from oscarapps.address.models import Locations
from oscarapps.catalogue.models import Product
from users.models import User


class BaseApplicationModel(models.Model):
    """
    An abstract base class model that common attributes
    """
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'influencers'
        abstract = True


class Influencers(BaseApplicationModel):
    """
    Information for each influencer
    """

    auto_id = models.CharField(unique=True, max_length=16, blank=True, null=True, default="", verbose_name=_('Influencer ID'))
    image = models.ImageField(upload_to='Influencers', null=True, blank=True)
    bio = models.TextField(blank=True, default="", verbose_name=_('Bio'))
    location = models.ForeignKey(Locations, null=True, blank=True, default="", verbose_name=_('Location'))
    users = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="influencers",blank=True, verbose_name=_("Users"))
    height = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.000'), verbose_name=_('Height'), help_text=_('US Measurements'))
    chest_or_bust = models.DecimalField(max_digits=10, decimal_places=3,default=Decimal('0.000'), verbose_name=_('Chest or Bust'), help_text=_('US Measurements'))
    hips = models.DecimalField(max_digits=10, decimal_places=3,default=Decimal('0.000'),  verbose_name=_('hips'), help_text=_('US Measurements'))
    waist = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.000'),  verbose_name=_('waist'), help_text=_('US Measurements'))

    def id_generator(self, size=10, chars=string.ascii_uppercase + string.digits):
        auto_id = ''.join(random.choice(chars) for _ in range(size))
        if auto_id not in Influencers.objects.values_list('auto_id', flat=True):
            return auto_id
        else:
            self.id_generator()

    def save(self, *args, **kwargs):
        super(Influencers, self).save(*args, **kwargs)
        if not self.auto_id:
            self.auto_id = self.id_generator()
            self.save()

    def __str__(self):

        return self.users.first_name


class InfluencerInvite(models.Model):
    email = models.EmailField(blank=True,null=True)
    code = models.CharField(max_length=20, blank=False,null=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def  __str__(self):
        return self.email


class InfluencerProductReserve(models.Model):

    influencer = models.ForeignKey(Influencers, blank=False, null=False, verbose_name=_('Influencer'))
    product = models.ForeignKey(Product, blank=False, null=False, verbose_name=_('Product'))
    date_reserved = models.DateTimeField(auto_now_add=True, verbose_name=_('Product Reserved Date'))

    class Meta:
        verbose_name_plural = _('Influencer Product Reservations')


class InfluencerProductRentedDetails(models.Model):
    influencer = models.ForeignKey(Influencers, blank=False, null=False, verbose_name=_('Influencer'))
    product = models.ForeignKey(Product, blank=False, null=False, verbose_name=_('Product'))
    date_reserved = models.DateTimeField(auto_now_add=True, verbose_name=_('Product Reserved Date'))

    class Meta:
        verbose_name_plural = _('Influencer Product-Rentals')

@receiver(pre_save, sender=Product, dispatch_uid="update_rental_date")
def update_influencer_product_rental_info(sender, instance, **kwargs):
    print("--------------------",instance.rental_status)
    print("=================", (Product.objects.get(pk=instance.pk)).rental_status)
    # try:
    current_obj = Product.objects.get(pk=instance.pk)
    influencer_product_reserve = InfluencerProductReserve.objects.filter(product=current_obj).values_list('influencer', flat=True)
    if len(influencer_product_reserve) > 0 :
        influencer_user = Influencers.objects.get(pk=influencer_product_reserve)

        if current_obj.rental_status != 'REN' and instance.rental_status == "REN":
            influencer_producted_rented_details = InfluencerProductRentedDetails()
            influencer_producted_rented_details.influencer = influencer_user
            influencer_producted_rented_details.product = current_obj
            influencer_producted_rented_details.save()
    # except:
    #     print("influencer product rental details updation error--->",instance)

pre_save.connect(update_influencer_product_rental_info, sender=Product, dispatch_uid="update_rental_date")


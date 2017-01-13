from oscar.apps.catalogue.abstract_models import AbstractProduct,AbstractCategory
from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscarapps.partner.models import Partner
from oscarapps.influencers.models import *

class BaseApplicationModel(models.Model):
    """
    An abstract base class model that common attributes
    """
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'Catalogue'
        abstract = True


class Category(AbstractCategory, BaseApplicationModel):
    pass




# class InfluencerProductInfo(models.Model):
#    influencers = models.ForeignKey('influencers.Influencers', null=True, verbose_name=_('Influencers'))
#    image = models.ImageField(upload_to='Influencer Product Images', null=True, blank=True)
#    influencer_note = models.TextField(blank=True, default="", verbose_name=_('Influencer Note'))
#

class Product(AbstractProduct, BaseApplicationModel):

   MALE = 'M'
   FEMALE = 'F'
   UNISEX = 'U'
   item_sex_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNISEX, 'Unisex'),
    )

   UNRESERVED = 'U'
   RESERVED = 'R'
   DRAFT = 'D'
   LIVE = 'L'
   status_choice = (
        (UNRESERVED, 'Unreserved'),
        (RESERVED, 'Reserved'),
        (DRAFT, 'Draft'),
        (LIVE, 'Live')
   )

   NONE = "NON"
   RENTED = 'REN'
   RETURNED = 'RET'
   rental_status_choice = (
        (NONE, 'None'),
        (RENTED, 'Rented'),
        (RETURNED, 'Returned'),
   )

   YES = 'Y'
   NO = 'N'
   shipping_choice = (
        (YES, 'Yes'),
        (NO, 'No'),
   )
   brand = models.ForeignKey(Partner, blank=True, null=True, default="", verbose_name="Brand")
   asin_id = models.CharField(blank=True, null=True, max_length=50, default="", verbose_name=_('ASIN'))
   gcid_id = models.CharField(blank=True, null=True, max_length=50,  default="", verbose_name=_('GCID'))
   gtnn_id = models.CharField(blank=True, null=True, max_length=50, default="", verbose_name=_('GTNN'))
   ups_id = models.CharField(blank=True, null=True, max_length=50, default="", verbose_name=_('UPS'))
   material_info = models.TextField(blank=True, default="", verbose_name=_('Material Information'))
   size = models.IntegerField(null=True, blank=True)
   wieght = models.IntegerField(null=True, blank=True)
   likes = models.IntegerField(default=0)
   on_sale = models.BooleanField(default=True, verbose_name=_('Product on sale'))
   item_sex_type = models.CharField(
        max_length=1,
        choices=item_sex_choice,
        default=UNISEX,
   )
   status = models.CharField(
        max_length=1,
        choices=status_choice,
        default=UNRESERVED,
        verbose_name=_("Status")
   )
   rental_status = models.CharField(
        max_length=3,
        choices=rental_status_choice,
        default=NONE,
        verbose_name=_("Rental Status")
   )
   requires_shipping = models.CharField(
        max_length=1,
        choices=shipping_choice,
        default=YES,
        verbose_name=_('Requires shipping.?')
   )

   #Metadata
   class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

   def __str__(self):
        return "{0}".format( self.title )

from oscar.apps.catalogue.models import *
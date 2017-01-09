from oscar.apps.catalogue.abstract_models import AbstractProduct,AbstractCategory
from django.db import models
from django.utils.translation import ugettext_lazy as _



from applications.models import currencies
from oscarapps.influencers.models import *

class Category(AbstractCategory):
    pass

# class Colors(models.Model):
#    color = models.CharField(null=True, max_length=10, blank=True, verbose_name=_('Color'))
#
#    def __str__(self):
#         return "{0}".format( self.color )




# class InfluencerProductInfo(models.Model):
#    influencers = models.ForeignKey('influencers.Influencers', null=True, verbose_name=_('Influencers'))
#    image = models.ImageField(upload_to='Influencer Product Images', null=True, blank=True)
#    influencer_note = models.TextField(blank=True, default="", verbose_name=_('Influencer Note'))
#

class Product(AbstractProduct):
   MALE = 'M'
   FEMALE = 'F'
   UNISEX = 'U'
   item_sex_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNISEX, 'Unisex'),
    )

   UNSELECTED = 'U'
   SELECTED = 'S'
   DRAFT = 'D'
   LIVE = 'L'
   status_choice = (
        (UNSELECTED, 'Unselected'),
        (SELECTED, 'Selected'),
        (DRAFT, 'Draft'),
        (LIVE, 'Live')
    )

   RENTED = 'REN'
   RETURNED = 'RET'
   rental_status_choice = (
        (RENTED, 'Rented'),
        (RETURNED, 'Returned'),
    )


   material_info = models.TextField(blank=True, default="", verbose_name=_('Material Information'))
   size_and_fit_description = models.TextField(blank=True, default="", verbose_name=_('Size And Fit Information'))
   size = models.IntegerField(null=True)
   item_sex_type = models.CharField(
        max_length=1,
        choices=item_sex_choice,
        default=UNISEX,
   )
   likes = models.IntegerField(default=0)
   created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
   modified = models.DateTimeField(auto_now=True, blank=True, null=True)
   status = models.CharField(
        max_length=1,
        choices=status_choice,
        default=UNSELECTED,
   )
   rental_status = models.CharField(
        max_length=3,
        choices=rental_status_choice,
        default=RENTED,
   )
   # color = models.ManyToManyField(Colors, null=True, blank=True, verbose_name=_('Color(s)'))


   #old fields
   # product_url = models.URLField(max_length=100, blank=False,  default="",
   #      help_text=_('Enter the product url to the particular item on your website'), verbose_name=_('Product Url'))
   # currency = models.CharField(max_length=100, blank=True, choices=currencies, default="USD", verbose_name=_('Currency'))
   # isActive = models.BooleanField(default=False, verbose_name=_('Product Active'),
   #      help_text=_('Check to display your product on the app, uncheck to undisplay your product on the app'))





   #Metadata
   class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

   def __str__(self):
        return "{0}".format( self.product_name )







from oscar.apps.catalogue.models import *
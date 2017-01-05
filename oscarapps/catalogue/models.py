from oscar.apps.catalogue.abstract_models import AbstractProduct,AbstractCategory
from django.db import models
from django.utils.translation import ugettext_lazy as _



from applications.models import currencies



class Category(AbstractCategory):
    pass



class Product(AbstractProduct):
   MALE = 'M'
   FEMALE = 'F'
   UNISEX = 'U'
   item_sex_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNISEX, 'Unisex'),
    )
   color = models.CharField(unique=True, max_length=10, blank=True, default="", verbose_name=_('Color'))
   care_info_description = models.TextField(blank=True, default="", verbose_name=_('Care Information'))
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



   #old fields
   product_url = models.URLField(max_length=100, blank=False,  default="",
        help_text=_('Enter the product url to the particular item on your website'), verbose_name=_('Product Url'))
   product_currency = models.CharField(max_length=100, blank=True, choices=currencies, default="USD", verbose_name=_('Currency'))
   product_isActive = models.BooleanField(default=False, verbose_name=_('Product Active'),
        help_text=_('Check to display your product on the app, uncheck to undisplay your product on the app'))

   # brand = models.ForeignKey('Brand', null=True, help_text=_('Select Your Brand'), verbose_name=_('Label Name'))


   #Metadata
   class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

   def __str__(self):
        return "{0}".format( self.product_name )







from oscar.apps.catalogue.models import *
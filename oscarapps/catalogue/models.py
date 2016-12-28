from oscar.apps.catalogue.abstract_models import AbstractProduct,AbstractCategory
from django.db import models
from django.utils.translation import ugettext_lazy as _

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

from oscar.apps.catalogue.models import *
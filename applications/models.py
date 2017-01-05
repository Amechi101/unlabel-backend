# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from cloudinary.models import CloudinaryField

from applications.mixins import ValidateModelMixin
from django.core.urlresolvers import reverse
from applications.utils.model_fields import CurrencyField, currencies, styles, categories

import uuid

class BaseApplicationModel(models.Model):
    """
    An abstract base class model that common attributes
    """
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'Applications'
        abstract = True


class Brand(BaseApplicationModel):
    """
    Information for each brand
    """
    
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # General information
    brand_name = models.CharField(unique=True, max_length=100, blank=True, default="", verbose_name=_('Brand Name'))
    brand_description = models.TextField(blank=True, default="", verbose_name=_('Description'))
    brand_feature_image = CloudinaryField('Featured Brand Image', null=True, blank=True)
    brand_website_url = models.URLField(max_length=100, default="", blank=True, verbose_name=_('Website'))
    
    # location
    brand_city = models.ForeignKey('City', null=True, blank=True, default="")

    # activation
    brand_isActive = models.BooleanField(default=False, verbose_name=_('Brand Active'), 
        help_text=_('Check to activate brand'))

    # sex
    menswear = models.BooleanField(default=False, verbose_name=_('Men'), help_text=_('Menswear'))
    womenswear = models.BooleanField(default=False, verbose_name=_('Women'), help_text=_('Womenswear'))

    # category
    brand_category =  models.ManyToManyField('Category', blank=True, verbose_name=_('Category'))

    # style
    brand_style = models.ManyToManyField('Style', blank=True, verbose_name=_('Style'))

    # slug
    slug = models.SlugField(max_length=255, verbose_name=_('Brand Slug'), default="", blank=True)


    # Metadata
    class Meta: 
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return "{0}".format( self.brand_name )

    def get_absolute_url(self):
        return reverse('brand_detail', args=[self.slug])

    def clean(self):
        for field in self._meta.fields:

            value = getattr(self, field.name)
            
            if field.name == 'brand_name':
                try:
                    setattr(self, field.name, value.strip())
                    
                    setattr(self, field.name, value.lower())

                except Exception:
                    pass

    def save(self, *args, **kwargs):
        self.slug = slugify(self.brand_name)
        
        self.full_clean()
        
        super(Brand, self).save(*args, **kwargs)

class Category(ValidateModelMixin, BaseApplicationModel):
    """
    List of Categories
    """
    name = models.CharField(unique=True, max_length=100, blank=True, verbose_name=_('Categories'))

    description = models.TextField(blank=True, default="", verbose_name=_('Description'))

    # Metadata
    class Meta: 
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return "{0}".format( self.name )

class Style(ValidateModelMixin, BaseApplicationModel):
    """
    List of Styles
    """
    name = models.CharField(unique=True, max_length=100, blank=True, verbose_name=_('Style'))

    description = models.TextField(blank=True, default="", verbose_name=_('Description'))

    # Metadata
    class Meta: 
        verbose_name = _('Style')
        verbose_name_plural = _('Styles')

    def __str__(self):
        return "{0}".format( self.name )

class Location(ValidateModelMixin, BaseApplicationModel):
    """
    List of Locations
    """
    STATE = "State"
    COUNTRY = "Country"

    LOCATION_CHOICES = (
        (STATE, "U.S.A"),
        (COUNTRY, "International")
    )
    
    state_or_country = models.CharField(unique=True, max_length=200, blank=True, default="", verbose_name=_('Location'), 
        help_text=_('Enter your State (USA only) or Country (International only)'))
    
    location_choices = models.CharField(max_length=100, blank=True, choices=LOCATION_CHOICES, verbose_name=_('U.S.A or International'))

    # Metadata
    class Meta: 
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __str__(self):
        return "{0}".format( self.state_or_country )

class City(ValidateModelMixin, BaseApplicationModel):
    """
    List of cities
    """
    city = models.CharField(unique=True, max_length=200, blank=True, default="", verbose_name=_('City') )

    latitude = models.DecimalField(max_digits=8, decimal_places=5,
        null=True, blank=True)
    
    longitude = models.DecimalField(max_digits=8, decimal_places=5,
        null=True, blank=True)

    # Foreign Key
    location = models.ForeignKey('Location', null=True, blank=True, help_text=_('Select your State or Country'), verbose_name=_('Location'))

    # Metadata
    class Meta: 
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return "{0}, {1}".format( self.city, self.location )


##################### Rethink for ecommerce ###############################
class Product(BaseApplicationModel):
    """
    Product for each brand
    """

    product_name = models.CharField(max_length=100, blank=False, default="", verbose_name=_('Product Name') )
    product_url = models.URLField(max_length=100, blank=False,  default="",
        help_text=_('Enter the product url to the particular item on your website'), verbose_name=_('Product Url'))
    product_price = CurrencyField( verbose_name=_('Product Price'),  blank=False )
    product_currency = models.CharField(max_length=100, blank=True, choices=currencies, default="USD", verbose_name=_('Currency'))
    product_image = CloudinaryField('Product Image', blank=False,  null=True)
    product_isActive = models.BooleanField(default=False, verbose_name=_('Product Active'),
        help_text=_('Check to display your product on the app, uncheck to undisplay your product on the app'))

    # Foreign Key
    brand = models.ForeignKey('Brand', null=True, help_text=_('Select Your Brand'), verbose_name=_('Label Name'))

    product_isMale = models.BooleanField(default=False, verbose_name=_('Product isMale'),
        help_text=_('''Check to denote this product is for men. This is 
            an advance option and only meant if your label sells men & women products'''))
    
    product_isFemale = models.BooleanField(default=False, verbose_name=_('Product isFemale'),
        help_text=_('''Check to denote this product is for women. This is 
            an advance option and only meant if your label sells men & women products'''))

    product_isUnisex = models.BooleanField(default=False, verbose_name=_('Product isUnisex'),
        help_text=_('''Check to denote this product is for men & women. This is 
            an advance option and only meant if your label sells men & women products'''))

    #Metadata
    class Meta: 
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return "{0}".format( self.product_name )
####################################################

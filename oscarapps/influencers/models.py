# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from oscar.core.compat import AUTH_USER_MODEL
from django.template.defaultfilters import slugify
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from oscarapps.influencers.mixins import ValidateModelMixin

from cloudinary.models import CloudinaryField

from applications.models import Brand
from oscarapps.address.models import Locations
from oscarapps.partner.models import Style
class BaseApplicationModel(models.Model):
    """
    An abstract base class model that common attributes
    """
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'Influencers'
        abstract = True


class Industry(models.Model):
    name = models.CharField(unique=True, max_length=100, blank=True, verbose_name=_('Industry Preference'))
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))

    # Metadata
    class Meta:
        verbose_name = _('Industry Preference')
        verbose_name_plural = _('Industry Preferences')

    def __str__(self):
        return self.name


class InfluencerPhysicalAttributes(models.Model):

    height = models.DecimalField(max_digits=10, decimal_places=3, blank=True, verbose_name=_('Height'), help_text=_('US Measurements'))
    chest_or_bust = models.DecimalField(max_digits=10, decimal_places=3, blank=True, verbose_name=_('Chest or Bust'), help_text=_('US Measurements'))
    hips = models.DecimalField(max_digits=10, decimal_places=3, blank=True, verbose_name=_('hips'), help_text=_('US Measurements'))
    waist = models.DecimalField(max_digits=10, decimal_places=3, blank=True, verbose_name=_('waist'), help_text=_('US Measurements'))
    shoe_size = models.DecimalField(max_digits=10, decimal_places=3, blank=True, verbose_name=_('shoe_size'), help_text=_('US Measurements'))




class Influencers(BaseApplicationModel):
    """
    Information for each influencer
    """


    name = models.CharField(max_length=100, blank=True, default="", verbose_name=_('Name'))
    image = models.ImageField(upload_to='Influencers', null=True, blank=True)
    bio = models.TextField(blank=True, default="", verbose_name=_('Bio'))
    physical_attributes = models.ManyToManyField('InfluencerPhysicalAttributes', blank=True, verbose_name=_('Physical Attributes'))

    location = models.ForeignKey(Locations, null=True, blank=True, default="", verbose_name=_('Location'))

    users = models.ManyToManyField(
        AUTH_USER_MODEL, related_name="influencers",
        blank=True, verbose_name=_("Users"))
    
    # industry_choice = models.ManyToManyField(Industry, blank=True, verbose_name='Industry Preferences')
    # style_Preference = models.ManyToManyField(Style, blank=True, verbose_name=_('Style Preferences'))
    # isActive = models.BooleanField(default=False, verbose_name=_('Influencer active'),
    #     help_text=_('Check to activate influencer'))
    # slug = models.SlugField(max_length=255, verbose_name=_('Influencer Slug'), default="", blank=True)
    # instagram_url = models.URLField(max_length=255, blank=True, default="", verbose_name=_('Instagram url'))
    # website_url = models.URLField(max_length=255, blank=True, default="", verbose_name=_('Website url'))

    #Old wanted Fields
    #influencer_isActive = models.BooleanField(default=False, verbose_name=_('Influencer active'),
    #instagram_handle = models.CharField(max_length=100, blank=True, default="", verbose_name=_('Instagram handle'))
    # hometown = models.ForeignKey('City', null=True, blank=True, default="", verbose_name=_('Hometown'))
    # website_name = models.CharField(max_length=100, blank=True, default="", verbose_name=_('Website name'))
    # website_isActive = models.BooleanField(default=False, verbose_name=_('Website active'),
    #     help_text=_('Check to activate website'))
    # photographer_credit_isActive = models.BooleanField(default=False, verbose_name=_('Photographer credit active'),
    #     help_text=_('Check to activate photographer credit'))

    #brand
    # brands = models.ForeignKey(Brand, null=True, blank=True, default="", help_text=_('Please select your brand'), verbose_name=_('Brand name'),
    #     related_name='brands')
    # question_brand_attraction = models.TextField(blank=True, default="", verbose_name=_('Brand attraction'))

    #product
    # question_product_favorite_name = models.CharField(max_length=255, blank=True, default="", verbose_name=_('Favorite product name'))
    # question_product_favorite_explanation = models.TextField(blank=True, default="", verbose_name=_('Favorite product explanation'))
    # question_product_favorite_url = models.URLField(max_length=255, blank=True, default="", verbose_name=_('Favorite product url'))
    # question_product_favorite_product_pairing = models.TextField(blank=True, default="", verbose_name=_('Product pairing explanation'))

    #personal style
    # question_personal_style_one = models.CharField(max_length=255, blank=True, default="", verbose_name=_('Personal style 1'))

    # other questions
    # question_fashion_advice = models.TextField(blank=True, default="", verbose_name=_('Fashion advice'))
    # question_favorite_season = models.TextField(blank=True, default="", verbose_name=_('Favorite season'))

    # Metadata
    class Meta:
        verbose_name = _('Influencer')
        verbose_name_plural = _('Influencers')

    def __str__(self):
        return "{0}".format( self.name )

    # def get_absolute_url(self):
    #     return reverse('influencer_detail', args=[self.slug])

    # def clean(self):
    #     for field in self._meta.fields:
    #
    #         value = getattr(self, field.name)
    #
    #         if field.name == 'name' or field.name == 'instagram_handle' or field.name == 'website_name':
    #             try:
    #                 setattr(self, field.name, value.strip())
    #
    #                 setattr(self, field.name, value.lower())
    #
    #             except Exception:
    #                 pass
    #
    # def save(self, *args, **kwargs):
    #
    #     self.slug = slugify(self.name)
    #
    #     self.full_clean()
    #
    #     super(Influencers, self).save(*args, **kwargs)


# class City(ValidateModelMixin, BaseApplicationModel):
#     """
#     List of cities
#     """
#     city = models.CharField(unique=True, max_length=200, blank=True, default="", verbose_name=_('City') )
#
#     # Foreign Key
#     state_or_country = models.ForeignKey('StateCountry', null=True, blank=True, help_text=_('Select your state or country'), verbose_name=_('State or Country'))
#
#     # Metadata
#     class Meta:
#         verbose_name = _('City')
#         verbose_name_plural = _('Cities')
#
#     def __str__(self):
#         return "{0}, {1}".format( self.city, self.state_or_country )
#
# class StateCountry(ValidateModelMixin, BaseApplicationModel):
#     """
#     List of Locations
#     """
#     STATE = "State"
#     COUNTRY = "Country"
#
#     LOCATION_CHOICES = (
#         (STATE, "U.S.A"),
#         (COUNTRY, "International")
#     )
#
#     name = models.CharField(unique=True, max_length=200, blank=True, default="", verbose_name=_('Location'),
#         help_text=_('Enter your State (USA only) or Country (International only)'))
#
#     location_choice = models.CharField(max_length=100, blank=True, choices=LOCATION_CHOICES, verbose_name=_('U.S.A or International'))
#
#     # Metadata
#     class Meta:
#         verbose_name = _('State or Country')
#         verbose_name_plural = _('State or Country')
#
#     def __str__(self):
#         return "{0}".format( self.name )


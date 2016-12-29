# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template.defaultfilters import slugify
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from influencers.mixins import ValidateModelMixin

from cloudinary.models import CloudinaryField

from applications.models import Brand
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


class Influencers(BaseApplicationModel):
    """
    Information for each influencer
    """
    
    #General info
    name = models.CharField(max_length=100, blank=True, default="", verbose_name=_('Influencer name'))

    # instagram_handle = models.CharField(max_length=100, blank=True, default="", verbose_name=_('Instagram handle'))

    instagram_url = models.URLField(max_length=255, blank=True, default="", verbose_name=_('Instagram url'))

    # hometown = models.ForeignKey('City', null=True, blank=True, default="", verbose_name=_('Hometown'))

    website_url = models.URLField(max_length=255, blank=True, default="", verbose_name=_('Website url'))

    # website_name = models.CharField(max_length=100, blank=True, default="", verbose_name=_('Website name'))

    # website_isActive = models.BooleanField(default=False, verbose_name=_('Website active'),
    #     help_text=_('Check to activate website'))
    #
    # image = CloudinaryField('Influencer Image', null=True, blank=True)

    # photographer_credit = models.CharField(max_length=255, blank=True, default="", verbose_name=_('Photographer credit'),
    #     help_text=_('To give credit for photographer for image'))

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
    bio = models.TextField(blank=True, default="", verbose_name=_('Bio'))
    #slug
    # slug = models.SlugField(max_length=255, verbose_name=_('Influencer Slug'), default="", blank=True)

    # active
    influencer_isActive = models.BooleanField(default=False, verbose_name=_('Influencer active'), 
        help_text=_('Check to activate influencer'))
    style_Preference = models.ManyToManyField(Style, blank=True, verbose_name=_('Style Preference'))

    # Metadata
    class Meta: 
        verbose_name = _('Influencer')
        verbose_name_plural = _('Influencers')

    def __str__(self):
        return "{0}".format( self.name )

    def get_absolute_url(self):
        return reverse('influencer_detail', args=[self.slug])

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

    def save(self, *args, **kwargs):

        self.slug = slugify(self.name)
        
        self.full_clean()
        
        super(Influencers, self).save(*args, **kwargs)


class City(ValidateModelMixin, BaseApplicationModel):
    """
    List of cities
    """
    city = models.CharField(unique=True, max_length=200, blank=True, default="", verbose_name=_('City') )

    # Foreign Key
    state_or_country = models.ForeignKey('StateCountry', null=True, blank=True, help_text=_('Select your state or country'), verbose_name=_('State or Country'))

    # Metadata
    class Meta: 
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return "{0}, {1}".format( self.city, self.state_or_country )

class StateCountry(ValidateModelMixin, BaseApplicationModel):
    """
    List of Locations
    """
    STATE = "State"
    COUNTRY = "Country"

    LOCATION_CHOICES = (
        (STATE, "U.S.A"),
        (COUNTRY, "International")
    )
    
    name = models.CharField(unique=True, max_length=200, blank=True, default="", verbose_name=_('Location'), 
        help_text=_('Enter your State (USA only) or Country (International only)'))
    
    location_choice = models.CharField(max_length=100, blank=True, choices=LOCATION_CHOICES, verbose_name=_('U.S.A or International'))

    # Metadata
    class Meta: 
        verbose_name = _('State or Country')
        verbose_name_plural = _('State or Country')

    def __str__(self):
        return "{0}".format( self.name )

from oscar.apps.partner.abstract_models import AbstractPartner
from oscarapps.catalogue.models import Category
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from applications.models import City
from applications.mixins import ValidateModelMixin


class Partner(AbstractPartner):
    MALE = 'M'
    FEMALE = 'F'
    BOTH = 'B'
    sex_type_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (BOTH, 'Both'),
    )
    brand_website_url = models.URLField(max_length=100, default="", blank=True, verbose_name=_('Website'))
    brand_description = models.TextField(blank=True, default="", verbose_name=_('Description'))
    brand_feature_image = models.ImageField(_('Image'), upload_to='uploads', blank=True,
                              null=True, max_length=255)
    brand_isActive = models.BooleanField(default=False, verbose_name=_('Brand Active'),
        help_text=_('Check to activate brand'))
    sex_type = models.CharField(
        max_length=1,
        choices=sex_type_choice,
        default=BOTH,
        verbose_name=_('Sex Type')
    )
    brand_style = models.ManyToManyField('Style', blank=True, verbose_name=_('Style Preference'))
    category = models.ManyToManyField(Category, blank=True, verbose_name=_('Category'))
    slug = models.SlugField(max_length=255, verbose_name=_('Brand Slug'), default="", blank=True)





    #old fields

    # location

    # brand_city = models.ForeignKey('City', null=True, blank=True, default="")


#old models

class Style(ValidateModelMixin, models.Model):
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



from oscar.apps.partner.models import *
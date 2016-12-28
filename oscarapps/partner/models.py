from oscar.apps.partner.abstract_models import AbstractPartner
from oscarapps.catalogue.models import Category
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

class Style(models.Model):
    """
    List of Styles
    """
    name = models.CharField(
        pgettext_lazy(u"Style's name", u"Name"), max_length=128, blank=True)
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))

    # Metadata
    def __str__(self):
        return "{0}".format( self.name )

class Partner(AbstractPartner):
    MALE = 'M'
    FEMALE = 'F'
    BOTH = 'B'
    sex_type_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (BOTH, 'Both'),
    )
    slug = models.SlugField(max_length=255, verbose_name=_('Brand Slug'), default="", blank=True)
    website_url = models.URLField(max_length=100, default="", blank=True, verbose_name=_('Website'))
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))
    image = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name=_('Brand Active'), help_text=_('Check to activate brand'))
    sex_type = models.CharField(
        max_length=1,
        choices=sex_type_choice,
        default=BOTH,
        verbose_name=_('Sex Type')
    )
    style_Preference = models.ManyToManyField(Style, blank=True, verbose_name=_('Style Preference'))
    category = models.ManyToManyField(Category, blank=True, verbose_name=_('Category'))

from oscar.apps.partner.models import *
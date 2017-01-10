from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.apps.address.abstract_models import AbstractAddress
from oscar.apps.partner.abstract_models import AbstractPartner
from django.core.validators import RegexValidator
from oscarapps.address.models import Locations
from oscar.apps.address.models import Country

class Style(models.Model):

    name = models.CharField(unique=True, max_length=100, blank=True, verbose_name=_('Style'))
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))

    # Metadata
    class Meta:
        verbose_name = _('Style')
        verbose_name_plural = _('Styles')

    def __str__(self):
        return "{0}".format( self.name )


class BrandStoreType(models.Model):

    store_type = models.CharField(unique=True, max_length=100, blank=True, verbose_name=_('Store Type'))

    # Metadata
    class Meta:
        verbose_name = _('Store Type')
        verbose_name_plural = _('Store Types')

    def __str__(self):
        return "{0}".format(self.store_type)


class BrandCategories(models.Model):

    categories = models.CharField(unique=True, max_length=100, blank=True, verbose_name=_('Category'))
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))
    type = models.ManyToManyField('BrandStoreType', blank=True, verbose_name=_('Brand Store Type'))

    # Metadata
    class Meta:
        verbose_name = _('Brand Category')
        verbose_name_plural = _('Brand Categories')

    def __str__(self):
        return "{0}".format(self.categories)


class BrandStyle(models.Model):

    name = models.CharField(unique=True, max_length=100, blank=True, verbose_name=_('Style'))
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))
    type = models.ManyToManyField('BrandStoreType', blank=True, verbose_name=_('Brand Store Type'))
    # Metadata
    class Meta:
        verbose_name = _('Brand Style')
        verbose_name_plural = _('Brand Styles')

    def __str__(self):
        return "{0}".format( self.name )


class AvailableDateTime(models.Model):
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()

    class Meta:
        verbose_name = _('Available Date And Time')

    def __str__(self):
        availabilty = str(self.date) + " From:" + str(self.from_time) + " To: " + str(self.to_time)
        return "{0}".format(availabilty)



class Partner(AbstractPartner):
    MALE = 'M'
    FEMALE = 'F'
    BOTH = 'B'
    sex_type_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (BOTH, 'Both'),
    )
    image = models.ImageField(_('Image'), upload_to='Brands', blank=True, null=True, max_length=255)
    location = models.ForeignKey(Locations, null=True, blank=True, default="", verbose_name=_('Location'))
    description = models.TextField(blank=True, default="", verbose_name=_('Brand Description'))
    sex_type = models.CharField(
        max_length=1,
        choices=sex_type_choice,
        default=BOTH,
        verbose_name=_('Sex Type')
    )
    style_preferences = models.ManyToManyField('Style', blank=True, verbose_name=_('Style Preference'))
    store_type = models.ManyToManyField('BrandStoreType', blank=True, verbose_name=_('Store Type'))
    store_categories = models.ManyToManyField('BrandCategories', blank=True, verbose_name=_('Store Categories'))
    isActive = models.BooleanField(default=True, verbose_name=_('Store Active'),
        help_text=_('Check|Un check to activate|deactivate store'))
    slug = models.SlugField(max_length=255, verbose_name=_('Brand Slug'), default="", blank=True)
    street_address = models.CharField(max_length=20, blank=True, default="", verbose_name=_('Street Address'))
    post_box = models.CharField(max_length=20, blank=True, default="", verbose_name=_('Apartment/P.O.Box') )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits are allowed.")
    city = models.CharField(max_length=20, default="", verbose_name=_('City'))
    state_province = models.CharField(max_length=20, default="", verbose_name=_('State/Province'))
    country = models.ForeignKey(Country, default="", verbose_name=_('Country'))
    contact_number = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    availability = models.ForeignKey('AvailableDateTime', null=True, blank=True, default="", verbose_name=_('Availability'))



from oscar.apps.partner.models import *
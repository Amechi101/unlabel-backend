from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.apps.address.abstract_models import AbstractAddress
from oscar.apps.partner.abstract_models import AbstractPartner
from django.core.validators import RegexValidator
from oscarapps.address.models import Locations,States
from oscar.apps.address.models import Country
# from django.contrib.auth.models import User
from django.conf import settings

class BaseApplicationModel(models.Model):
    """
    An abstract base class model that common attributes
    """
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'Partners'
        abstract = True


class Style(BaseApplicationModel):

    name = models.CharField(unique=True, max_length=100, blank=True, verbose_name=_('Style'))
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))

    # Metadata
    class Meta:
        verbose_name = _('Style')
        verbose_name_plural = _('Styles')

    def __str__(self):
        return "{0}".format( self.name )


class BrandStoreType(BaseApplicationModel):

    name = models.CharField(unique=True, max_length=100, blank=True, verbose_name=_('Store Type'))

    # Metadata
    class Meta:
        verbose_name = _('Store Type')
        verbose_name_plural = _('Store Types')

    def __str__(self):
        return "{0}".format(self.name)


class BrandCategories(BaseApplicationModel):

    name = models.CharField(unique=True, max_length=100, blank=True, verbose_name=_('Category'))
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))
    type = models.ManyToManyField('BrandStoreType', blank=True, verbose_name=_('Brand Category'))

    # Metadata
    class Meta:
        verbose_name = _('Brand Category')
        verbose_name_plural = _('Brand Categories')

    def __str__(self):
        return "{0}".format(self.name)


class BrandStyle(BaseApplicationModel):

    name = models.CharField(unique=True, max_length=100, blank=True, verbose_name=_('Style'))
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))
    type = models.ManyToManyField('BrandStoreType', blank=True, verbose_name=_('Brand Style'))
    # Metadata
    class Meta:
        verbose_name = _('Brand Style')
        verbose_name_plural = _('Brand Styles')

    def __str__(self):
        return "{0}".format(self.name)


class AvailableDateTime(BaseApplicationModel):
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()

    class Meta:
        verbose_name = _('Available Date And Time')

    def __str__(self):
        availabilty = str(self.date) + " From:" + str(self.from_time) + " To: " + str(self.to_time)
        return "{0}".format(availabilty)



class Partner(AbstractPartner, BaseApplicationModel):
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
    is_active = models.BooleanField(default=True, verbose_name=_('Store Active'),
        help_text=_('Check|Un check to activate|deactivate store'))
    slug = models.SlugField(max_length=255, verbose_name=_('Brand Slug'), default="", blank=True)
    street_address = models.CharField(max_length=20, blank=True, default="", verbose_name=_('Street Address'))
    post_box = models.CharField(max_length=20, blank=True, default="", verbose_name=_('Apartment/P.O.Box') )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits are allowed.")
    city = models.CharField(max_length=20, default="", verbose_name=_('City'))
    state = models.ForeignKey(States, default="", verbose_name=_('State'))
    zipcode = models.CharField(max_length=10, blank=True, null=True, default="", verbose_name=_('Zip code'))
    country = models.ForeignKey(Country, default="", verbose_name=_('Country'))
    contact_number = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    availability = models.ForeignKey('AvailableDateTime', null=True, blank=True, default="", verbose_name=_('Availability'))

    class Meta:
        verbose_name = _('Brands Detail')

class PartnerFollow(models.Model):
    customer = models.ForeignKey( settings.AUTH_USER_MODEL )
    partner = models.ForeignKey( Partner )

    class Meta:
        verbose_name = _('Brand Follows')
        verbose_name_plural = _('Brand Follows')

    def __str__(self):
        return self.customer.email+" --> "+self.partner.name



from oscar.apps.partner.models import *
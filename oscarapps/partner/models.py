from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings

from multiselectfield import MultiSelectField
from oscar.apps.partner.abstract_models import AbstractPartner
from users.models import User

from oscarapps.address.models import Locations



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

    class Meta:
        verbose_name = _('Style')
        verbose_name_plural = _('Styles')

    def __str__(self):
        return "{0}".format(self.name)


class Category(BaseApplicationModel):

    MENSWEAR = 'M'
    WOMENSWEAR = 'W'
    category_choice = (
        (MENSWEAR, 'Menswear'),
        (WOMENSWEAR, 'Womenswear'),
    )
    name = MultiSelectField(choices=category_choice)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return "{0}".format(self.name)


class SubCategory(BaseApplicationModel):
    name = models.CharField(unique=True, max_length=100, blank=True, verbose_name=_('Sub Category'))
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Sub Category')
        verbose_name_plural = _('Sub Categories')

    def __str__(self):
        return "{0}".format(self.name)

class ProfileInformation(User, BaseApplicationModel):

    class Meta:
        verbose_name = _('Profile Information')


class RentalTime(BaseApplicationModel):
    MONDAY = 'MO'
    TUESDAY = 'TU'
    WEDNESDAY = 'WE'
    THURSDAY = 'TH'
    FRIDAY = 'FR'
    SATURDAY = 'SA'
    SUNDAY = 'SU'
    day_choice = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )
    day = MultiSelectField(choices=day_choice)
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")

    class Meta:
        verbose_name = _('Rental Time')

    def __str__(self):

        return "{0}".format(self.day)


class RentalAddress(Locations):
    post_box = models.CharField(max_length=20, blank=True, default="", verbose_name=_('Apartment/P.O.Box'))
    zipcode = models.CharField(max_length=10, blank=True, null=True, default="", verbose_name=_('Zip code'))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: "
                                                                   "'+999999999'. Up to 15 digits are allowed.")
    contact_number = models.CharField(validators=[phone_regex], max_length=20, blank=True)


class Partner(AbstractPartner, BaseApplicationModel):
    slug = models.SlugField(max_length=255, default="", blank=True, verbose_name=_('Brand Slug'))
    image = models.ImageField(_('Image'), upload_to='Brands', blank=True, null=True, max_length=255)
    location = models.ForeignKey(Locations, null=True, blank=True, default="", related_name='get_partner', verbose_name=_('Location'))
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))
    style = models.ManyToManyField('Style', blank=True, verbose_name=_('Style'))
    category = models.ManyToManyField('Category', blank=True, verbose_name=_('Category'))
    sub_category = models.ManyToManyField('SubCategory', blank=True, verbose_name=_('Category'))
    profile_info = models.ManyToManyField(ProfileInformation, blank= True, verbose_name=_('Profile Information'))
    is_active = models.BooleanField(default=True, verbose_name=_('Store Active'),
                                    help_text=_('Check|Un check to activate|deactivate store'))
    rental_time = models.ForeignKey('RentalTime', null=True, blank=True, default="",
                                     verbose_name=_('Rental Time'))
    rental_address = models.ForeignKey('RentalAddress', null=True, blank=True, default="", verbose_name=_('Rental Address'))

    class Meta:
        verbose_name = _('Brands Detail')


class PartnerFollow(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL)
    partner = models.ForeignKey(Partner)

    class Meta:
        verbose_name = _('Brand Follows')
        verbose_name_plural = _('Brand Follows')

    def __str__(self):
        return self.customer.email+" --> "+self.partner.name



from oscar.apps.partner.models import *
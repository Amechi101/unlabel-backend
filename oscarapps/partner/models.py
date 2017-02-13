from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings

from multiselectfield import MultiSelectField
from oscar.apps.partner.abstract_models import AbstractPartner

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

    name = models.CharField(unique=True, max_length=100, verbose_name=_('Name'))
    description = models.TextField(blank=True, null=True, default="", verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Style')
        verbose_name_plural = _('Styles')

    def __str__(self):
        return "{0}".format(self.name)


class Category(BaseApplicationModel):

    MENSWEAR = 'Menswear'
    WOMENSWEAR = 'Womenswear'
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
    name = models.CharField(unique=True, max_length=100, verbose_name=_('Name'))
    description = models.TextField(blank=True, null=True, default="", verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Sub Category')
        verbose_name_plural = _('Sub Categories')

    def __str__(self):
        return "{0}".format(self.name)


class RentalInformation(Locations):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'
    day_choice = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )
    post_box = models.CharField(max_length=20, blank=True, null=True, default="", verbose_name=_('Apartment/P.O.Box'))
    zipcode = models.CharField(max_length=10, blank=True, null=True, default="", verbose_name=_('Zip code'))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: "
                                                                   "'+999999999'. Up to 15 digits are allowed.")
    contact_number = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    day = MultiSelectField(choices=day_choice)
    start_time = models.TimeField(blank=True, null=True, verbose_name=_("Start Time"))
    end_time = models.TimeField(blank=True, null=True, verbose_name=_("End Time"))

    class Meta:
        verbose_name = _('Rental Information')

    def __str__(self):

        return "{0}".format(self.day)

class Partner(AbstractPartner, BaseApplicationModel):
    slug = models.SlugField(max_length=255, default="", blank=True, null=True, verbose_name=_('Brand Slug'))
    image = models.ImageField(_('Image'), upload_to=_('Brands'), blank=True, null=True, max_length=255)
    location = models.ForeignKey(Locations, null=True, blank=True, default="", related_name=_('get_partner'),
                                 verbose_name=_('Location'))
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))
    style = models.ManyToManyField('Style', blank=True, verbose_name=_('Style'))
    category = models.ManyToManyField('Category', blank=True, verbose_name=_('Category'))
    sub_category = models.ManyToManyField('SubCategory', blank=True, verbose_name=_('Sub category'))
    is_active = models.BooleanField(default=True, verbose_name=_('Store Active'),
                                    help_text=_('Check|Un check to activate|deactivate store'))
    rental_info = models.ForeignKey('RentalInformation', null=True, blank=True, default="",
                                     verbose_name=_('Rental Informaton'))

    class Meta:
        app_label = 'partner'
        ordering = ('name', 'code')
        permissions = (('dashboard_access', 'Can access dashboard'), )
        verbose_name = _('Fulfillment partner')
        verbose_name_plural = _('Fulfillment partners')


class PartnerFollow(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name="Customer")
    partner = models.ForeignKey(Partner, blank=True, null=True, verbose_name="Partner")

    class Meta:
        verbose_name = _('Brand Follows')
        verbose_name_plural = _('Brand Follows')

    def __str__(self):
        return self.customer.email+" --> "+self.partner.name


class PartnerInvite(models.Model):
    email = models.EmailField(blank=True,null=True)
    code = models.CharField(max_length=20, blank=False,null=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def  __str__(self):
        return self.email


from oscar.apps.partner.models import *
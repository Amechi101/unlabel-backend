from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings

from multiselectfield import MultiSelectField
from oscar.apps.partner.abstract_models import AbstractPartner

from oscarapps.address.models import Locations
from django.template.defaultfilters import slugify


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

    MALE = 'Menswear'
    FEMALE = 'Womenswear'
    item_sex_choice = (
        (MALE, 'Menswear'),
        (FEMALE, 'Womenswear'),
    )

    name = models.CharField(max_length=10, choices=item_sex_choice, default=MALE,verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        if self.name == 'Menswear':
            value = "Menswear"
        elif self.name == 'Womenswear':
            value = "Womenswear"
        return value


class SubCategory(BaseApplicationModel):
    name = models.CharField(unique=True, max_length=100, verbose_name=_('Name'))
    description = models.TextField(blank=True, null=True, default="", verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Sub Category')
        verbose_name_plural = _('Sub Categories')

    def __str__(self):
        return "{0}".format(self.name)


class RentalTime(models.Model):
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

    AM = 'AM'
    PM = 'PM'
    time_period_choice = (
        (AM, 'AM'),
        (PM, 'PM'),
    )
    day = models.CharField(choices=day_choice, max_length=120)
    start_time = models.TimeField(blank=True, null=True, verbose_name=_("Start Time"))
    start_time_period = models.CharField(max_length=2, null=True, blank=True, choices=time_period_choice, verbose_name=_('Time Period'))
    end_time = models.TimeField(blank=True, null=True, verbose_name=_("End Time"))
    end_time_period = models.CharField(max_length=2, null=True, blank=True, choices=time_period_choice, verbose_name=_('Time Period'))

    class Meta:
        verbose_name = _('Rental Time')

    def __str__(self):

        return self.day
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(RentalTime, self).save()


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

    AM = 'AM'
    PM = 'PM'
    time_period_choice = (
        (AM, 'AM'),
        (PM, 'PM'),
    )
    post_box = models.CharField(max_length=20, blank=True, null=True, default="", verbose_name=_('Apartment/P.O.Box'))
    zipcode = models.CharField(max_length=10, blank=True, null=True, default="", verbose_name=_('Zip code'))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: "
                                                                   "'+999999999'. Up to 15 digits are allowed.")
    contact_number = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    day = MultiSelectField(choices=day_choice)
    start_time = models.TimeField(blank=True, null=True, verbose_name=_("Start Time"))
    start_time_period = models.CharField(max_length=2, null=True, blank=True, choices=time_period_choice, verbose_name=_('Time Period'))
    end_time = models.TimeField(blank=True, null=True, verbose_name=_("End Time"))
    end_time_period = models.CharField(max_length=2, null=True, blank=True, choices=time_period_choice, verbose_name=_('Time Period'))
    rental_time = models.ManyToManyField(RentalTime, null=True, blank=True)

    class Meta:
        verbose_name = _('Rental Information')

    def __str__(self):

        return "{0}".format(self.day)


class Partner(AbstractPartner, BaseApplicationModel):
    slug = models.SlugField(max_length=255, default="", blank=True, null=True, verbose_name=_('Brand Slug'))
    image = models.ImageField(_('Image'), upload_to='Brands', blank=True, null=True, max_length=255)
    location = models.ForeignKey(Locations, models.SET_NULL, null=True, blank=True, default="", related_name=_('partner_location'),
                                 verbose_name=_('Location'))
    description = models.TextField(blank=True, default="", verbose_name=_('Description'))
    style = models.ManyToManyField('Style', blank=True, verbose_name=_('Style'))
    category = models.ManyToManyField('Category', blank=True, verbose_name=_('Category'))
    sub_category = models.ManyToManyField('SubCategory', blank=True, verbose_name=_('Sub category'))
    is_active = models.BooleanField(default=True, verbose_name=_('Store Active'),
                                    help_text=_('Check|Un check to activate|deactivate store'))
    rental_info = models.ForeignKey('RentalInformation', models.SET_NULL, null=True, blank=True, default="",
                                     verbose_name=_('Rental Informaton'))
    follows = models.PositiveIntegerField(default=0,verbose_name=_('follow count'))

    class Meta:
        app_label = 'partner'
        ordering = ('name', 'code')
        permissions = (('dashboard_access', 'Can access dashboard'), )
        verbose_name = _('Fulfillment partner')
        verbose_name_plural = _('Fulfillment partners')
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Partner, self).save(*args, **kwargs)


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
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Locations(models.Model):
    STATE = "State"
    COUNTRY = "Country"

    LOCATION_CHOICES = (
        (STATE, "U.S.A"),
        (COUNTRY, "International")
    )
    city = models.CharField(unique=True, max_length=200, blank=True, default="", verbose_name=_('City') )
    state_or_country = models.CharField(unique=True, max_length=200, blank=True, default="", verbose_name=_('Location'),
        help_text=_('Enter your State (USA only) or Country (International only)'))
    location_choice = models.CharField(max_length=100, blank=True, choices=LOCATION_CHOICES, verbose_name=_('U.S.A or International'))
    latitude = models.DecimalField(max_digits=8, decimal_places=5,
        null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5,
        null=True, blank=True)




from oscar.apps.address.models import *

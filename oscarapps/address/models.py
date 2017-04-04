from django.db import models
from django.utils.translation import ugettext_lazy as _
from geopy.geocoders import Nominatim

from oscar.apps.address.models import Country

class States(models.Model):

    name = models.CharField(unique=True, max_length=100, blank=True, null=True, verbose_name=_('State'))

    class Meta:
        verbose_name = _('State in US')
        verbose_name_plural = _('States in US')

    def __str__(self):
        return self.name


class Locations(models.Model):
    city = models.CharField(max_length=200, default="", blank=False, null=False, verbose_name=_('City'))
    state = models.CharField(max_length=200, default="", blank=False, null=False, verbose_name=_('State'))
    country = models.CharField(max_length=200, default="", blank=False, null=False, verbose_name=_('Country'))
    # state = models.ForeignKey(States, models.SET_NULL, null=True, blank=True, default='', verbose_name=_('State'))
    # country = models.ForeignKey(Country, models.SET_NULL, null=True, blank=False, default="", verbose_name=_('Country'))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name=_('Latitude'))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name=_('Longitude'))
    is_brand_location = models.BooleanField(default=False, verbose_name=_('Brand Location'))
    is_influencer_location = models.BooleanField(default=False, verbose_name=_('Influencer Location'))

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __str__(self):
        location = str(self.city)+","+str(self.state)+","+str(self.country)
        return location
    """
    Function to find coordinates from address
    """
    def get_coordinates(self, address):
         try:
          geolocator = Nominatim()
          location = geolocator.geocode(address)
          return location.latitude, location.longitude
         except:
             return None, None


    def save(self, *args, **kwargs):
        address = str(self.city) + ","
        address += str(self.state) + ","
        address += str(self.country)
        self.latitude, self.longitude = self.get_coordinates(address)
        super(Locations, self).save(*args, **kwargs)


from oscar.apps.address.models import *

from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.apps.address.models import Country



class States(models.Model):

    state=models.CharField(unique=True,max_length=100,blank=True,null=True)

    class Meta:
        verbose_name = _('State in US')
        verbose_name_plural = _('States in US')

    def __str__(self):
        return self.state


class Locations(models.Model):

    city = models.CharField(max_length=200, default="", blank=False, null=False, verbose_name=_('City') )
    state=models.ForeignKey(States, null=True, blank=True, default='', verbose_name=_('State'))
    country=models.ForeignKey(Country, null=False, blank=False, default="", verbose_name=_('Country'))
    latitude = models.DecimalField(max_digits=8, decimal_places=5,
        null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5,
        null=True, blank=True)

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __str__(self):
        return self.country.name


from oscar.apps.address.models import *

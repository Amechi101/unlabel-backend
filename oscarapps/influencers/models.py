# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from oscarapps.address.models import Locations
import random
import string
from oscar.core.compat import get_user_model
User = get_user_model()

class BaseApplicationModel(models.Model):
    """
    An abstract base class model that common attributes
    """
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'influencers'
        abstract = True


class InfluencerAccountInfo(User, BaseApplicationModel):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits are allowed.")
    contact_number = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    def __str__(self):
        return self.firstname


class Influencers(BaseApplicationModel):
    """
    Information for each influencer
    """

    auto_id = models.CharField(unique=True, max_length=16, blank=True, null=True, default="", verbose_name=_('Influencer ID'))
    name = models.CharField(max_length=100, blank=True, default="", verbose_name=_('Name'))
    image = models.ImageField(upload_to='Influencers', null=True, blank=True)
    bio = models.TextField(blank=True, default="", verbose_name=_('Bio'))
    location = models.ForeignKey(Locations, null=True, blank=True, default="", verbose_name=_('Location'))
    users = models.ManyToManyField(
        InfluencerAccountInfo, related_name="influencers",
        blank=True, verbose_name=_("Users"))
    is_active = models.BooleanField(default=True, verbose_name=_('Activate/Deactivate Influencer'),
        help_text=_('Check to activate'))
    height = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, default="", verbose_name=_('Height'), help_text=_('US Measurements'))
    chest_or_bust = models.DecimalField(max_digits=10, decimal_places=3, null=True,  blank=True, default="", verbose_name=_('Chest or Bust'), help_text=_('US Measurements'))
    hips = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, default="",  verbose_name=_('hips'), help_text=_('US Measurements'))
    waist = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, default="",  verbose_name=_('waist'), help_text=_('US Measurements'))
    shoe_size = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, default="",  verbose_name=_('shoe_size'), help_text=_('US Measurements'))


    def id_generator(self, size=10, chars=string.ascii_uppercase + string.digits):
        id = ''.join(random.choice(chars) for _ in range(size))
        if id not in Influencers.objects.values_list('auto_id', flat=True):
            return id
        else:
            self.id_generator()

    def save(self, *args, **kwargs):
        super(Influencers, self).save(*args, **kwargs)
        if not self.auto_id:
            self.auto_id = self.id_generator()
            print(self.auto_id)
            self.save()

    def __str__(self):
        return self.name
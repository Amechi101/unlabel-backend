# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from oscar.core.compat import get_user_model
from django.core.validators import RegexValidator
from django.conf import settings
from oscarapps.address.models import Locations
from users.models import User



class BaseApplicationModel(models.Model):
    """
    An abstract base class model that common attributes
    """
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'influencers'
        abstract = True


class Influencers(BaseApplicationModel):
    """
    Information for each influencer
    """

    auto_id = models.CharField(unique=True, max_length=16, blank=True, null=True, default="", verbose_name=_('Influencer ID'))
    image = models.ImageField(upload_to='Influencers', null=True, blank=True)
    bio = models.TextField(blank=True, default="", verbose_name=_('Bio'))
    location = models.ForeignKey(Locations, null=True, blank=True, default="", verbose_name=_('Location'))
    users = models.OneToOneField(
        User, related_name="influencers",
        blank=True, verbose_name=_("Users"))
    height = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, default="", verbose_name=_('Height'), help_text=_('US Measurements'))
    chest_or_bust = models.DecimalField(max_digits=10, decimal_places=3, null=True,  blank=True, default="", verbose_name=_('Chest or Bust'), help_text=_('US Measurements'))
    hips = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, default="",  verbose_name=_('hips'), help_text=_('US Measurements'))
    waist = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, default="",  verbose_name=_('waist'), help_text=_('US Measurements'))

    def id_generator(self, size=10, chars=string.ascii_uppercase + string.digits):
        auto_id = ''.join(random.choice(chars) for _ in range(size))
        if auto_id not in Influencers.objects.values_list('auto_id', flat=True):
            return auto_id
        else:
            self.id_generator()

    def save(self, *args, **kwargs):
        super(Influencers, self).save(*args, **kwargs)
        if not self.auto_id:
            self.auto_id = self.id_generator()
            print(self.auto_id)
            self.save()

    def __str__(self):
        return self.users.email


class InfluencerInvite(models.Model):
    email = models.EmailField(blank=True,null=True)
    code = models.CharField(max_length=20, blank=False,null=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def  __str__(self):
        return self.user.email
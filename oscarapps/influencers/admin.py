from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from oscarapps.influencers.models import Influencers, InfluencerInvite

admin.site.register(Influencers)
admin.site.register(InfluencerInvite)








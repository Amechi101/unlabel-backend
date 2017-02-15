from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from oscarapps.influencers.models import Influencers, InfluencerInvite,InfluencerProductReserve

admin.site.register(Influencers)
admin.site.register(InfluencerInvite)
admin.site.register(InfluencerProductReserve)








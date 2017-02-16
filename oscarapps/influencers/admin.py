from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from .models import Influencers, InfluencerInvite,InfluencerProductReserve,InfluencerProductRentedDetails


admin.site.register(Influencers)
admin.site.register(InfluencerInvite)
admin.site.register(InfluencerProductReserve)
admin.site.register(InfluencerProductRentedDetails)










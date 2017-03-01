from .models import CommissionConfiguration,\
    InfluencerCommission,\
    BrandCommission,\
    UnlabelCommission,\
    StripeCredential,\
    Payout
from django.contrib import admin

admin.site.register(CommissionConfiguration)
admin.site.register(InfluencerCommission)
admin.site.register(BrandCommission)
admin.site.register(UnlabelCommission)
admin.site.register(StripeCredential)
admin.site.register(Payout)

from oscar.apps.payment.admin import *  # noqa

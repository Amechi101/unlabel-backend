from .models import CommissionConfiguration,\
    InfluencerCommission,\
    BrandCommission,\
    UnlabelCommission,\
    StripeCredential,\
    InfluencerPayout,\
    BrandPayout
from django.contrib import admin


class BrandPayoutAdmin(admin.ModelAdmin):
    list_filter = ['is_completed', 'created']


class InfluencerPayoutAdmin(admin.ModelAdmin):
    list_filter = ['is_completed', 'created']

admin.site.register(CommissionConfiguration)
admin.site.register(InfluencerCommission)
admin.site.register(BrandCommission)
admin.site.register(UnlabelCommission)
admin.site.register(StripeCredential)
admin.site.register(BrandPayout, BrandPayoutAdmin)
admin.site.register(InfluencerPayout, InfluencerPayoutAdmin)

from oscar.apps.payment.admin import *  # noqa

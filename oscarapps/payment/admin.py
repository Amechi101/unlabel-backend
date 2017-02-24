from .models import CommissionConfiguration,InfluencerCommission,BrandCommission,UnlabelCommission
from django.contrib import admin

admin.site.register(CommissionConfiguration)
admin.site.register(InfluencerCommission)
admin.site.register(BrandCommission)
admin.site.register(UnlabelCommission)


from oscar.apps.payment.admin import *  # noqa

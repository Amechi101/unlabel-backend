from django.contrib import admin
from oscar.core.loading import get_model

BrandStyle = get_model('partner', 'Style')
BrandCategories = get_model('partner', 'Category')
BrandSubCategories = get_model('partner', 'SubCategory')
BrandFollow = get_model('partner', 'PartnerFollow')
RentalInformation = get_model('partner', 'RentalInformation')
PartnerInvite = get_model('partner', 'PartnerInvite')
RentalTime = get_model('partner', 'RentalTime')

admin.site.register(BrandStyle)
admin.site.register(BrandCategories)
admin.site.register(BrandSubCategories)
admin.site.register(BrandFollow)
admin.site.register(RentalInformation)
admin.site.register(PartnerInvite)
admin.site.register(RentalTime)



from oscar.apps.partner.admin import *
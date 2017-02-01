from django.contrib import admin
from oscar.core.loading import get_model

BrandStyle = get_model('partner', 'Style')
BrandCategories = get_model('partner', 'Category')
BrandSubCategories = get_model('partner', 'SubCategory')
RentalAddress = get_model('partner', 'RentalAddress')
RentalTime = get_model('partner', 'RentalTime')
BrandFollow = get_model('partner', 'PartnerFollow')

admin.site.register(BrandStyle)
admin.site.register(BrandCategories)
admin.site.register(BrandSubCategories)
admin.site.register(RentalAddress)
admin.site.register(RentalTime)
admin.site.register(BrandFollow)



from oscar.apps.partner.admin import *
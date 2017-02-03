from django.contrib import admin
from oscar.core.loading import get_model

BrandStyle = get_model('partner', 'Style')
BrandCategories = get_model('partner', 'Category')
BrandSubCategories = get_model('partner', 'SubCategory')
BrandFollow = get_model('partner', 'PartnerFollow')
RentalInformation = get_model('partner', 'RentalInformation')

admin.site.register(BrandStyle)
admin.site.register(BrandCategories)
admin.site.register(BrandSubCategories)
admin.site.register(BrandFollow)
admin.site.register(RentalInformation)



from oscar.apps.partner.admin import *
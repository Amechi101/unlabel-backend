from django.contrib import admin
from oscar.core.loading import get_model

Style = get_model('partner', 'Style')
BrandStoreType = get_model('partner', 'BrandStoreType')
BrandCategories = get_model('partner', 'BrandCategories')
AvailableDateTime = get_model('partner', 'AvailableDateTime')

class StyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


admin.site.register(Style, StyleAdmin)
admin.site.register(BrandStoreType)
admin.site.register(BrandCategories)
admin.site.register(AvailableDateTime)


from oscar.apps.partner.admin import *
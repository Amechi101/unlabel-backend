from django.contrib import admin
from oscarapps.catalogue.models import SizeClass, Size,InfluencerProductImage

class SizeAdmin(admin.ModelAdmin):
    list_filter = ['size', 'size_class', 'size_sex_type', ]
    list_display = ['size', 'size_sex_type', 'size_class', ]


admin.site.register(Size, SizeAdmin)
admin.site.register(SizeClass)
admin.site.register(InfluencerProductImage)
from oscar.apps.catalogue.admin import *  # noqa

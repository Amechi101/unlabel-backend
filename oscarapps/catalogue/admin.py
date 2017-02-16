from django.contrib import admin
from oscarapps.catalogue.models import SizeClass, Size

class SizeAdmin(admin.ModelAdmin):
    list_filter = ['size', 'size_class', 'size_sex_type', ]
    list_display = ['size', 'size_sex_type', 'size_class', ]


admin.site.register(Size, SizeAdmin)
admin.site.register(SizeClass)
from oscar.apps.catalogue.admin import *  # noqa

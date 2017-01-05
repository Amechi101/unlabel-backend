from django.contrib import admin
from oscar.core.loading import get_model

Style = get_model('partner', 'Style')

class StyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)

admin.site.register(Style, StyleAdmin)

from oscar.apps.partner.admin import *
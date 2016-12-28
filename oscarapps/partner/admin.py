from django.contrib import admin
from .models import Style
admin.site.register(Style)
from oscar.apps.partner.admin import *  # noqa

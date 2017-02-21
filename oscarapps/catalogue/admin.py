from django.contrib import admin
from oscarapps.catalogue.models import InfluencerProductImage

admin.site.register(InfluencerProductImage)
from oscar.apps.catalogue.admin import *  # noqa

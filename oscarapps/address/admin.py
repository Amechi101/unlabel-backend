from oscar.apps.address.admin import *  # noqa
from .models import States, Locations

admin.site.register(States)
admin.site.register(Locations)
from oscar.apps.address.admin import *  # noqa
from .models import States, Locations, TelephoneCode

admin.site.register(States)
admin.site.register(Locations)
admin.site.register(TelephoneCode)
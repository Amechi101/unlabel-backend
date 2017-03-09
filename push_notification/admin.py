from django.contrib import admin
from .models import APNSDevice,NotificationDetails

admin.site.register(APNSDevice)
admin.site.register(NotificationDetails)


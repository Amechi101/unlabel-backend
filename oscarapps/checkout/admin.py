import stripe
from django.contrib import admin
# from stripe import Token, Recipient, Transfer
from oscarapps.checkout.models import Sale, Pay

admin.site.register(Sale)
admin.site.register(Pay)
# admin.site.register(Token)
# admin.site.register(Recipient)
# admin.site.register(Transfer)
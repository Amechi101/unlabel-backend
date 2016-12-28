from oscar.apps.customer.admin import *  # noqa
from .models import EmailConfirmation

admin.site.register(EmailConfirmation)
from oscar.apps.customer.models import *
from oscar.apps.customer.abstract_models import AbstractUser
from django.db import models

# class EmailConfirmation(models.Model):
#    email = models.EmailField(max_length=250,verbose_name='Email')
#    key = models.CharField(max_length=255, verbose_name='Hash Key')
#    created_time = models.DateTimeField("Created Date", auto_now_add=True)
#    link_expired = models.BooleanField(default=False, verbose_name='Link Expired')
#
#    def __str__(self):
#        return self.email

from oscar.apps.customer.models import *
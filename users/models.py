from django.db import models
from oscar.apps.customer.abstract_models import AbstractUser


class User(AbstractUser):


    def get_full_name(self):
        full_name = '%s %s' % (self.last_name.upper(), self.first_name)
        return full_name.strip()

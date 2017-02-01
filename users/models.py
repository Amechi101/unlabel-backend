from django.db import models

from oscar.apps.customer.abstract_models import AbstractUser


class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    sex_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    contact_number = models.CharField(max_length=20, blank=True, null=True)
    is_influencer = models.BooleanField(default=False)
    gender = models.CharField(choices=sex_choice, max_length=1, null=True, blank=True)
    def get_full_name(self):
        full_name = '%s %s' % (self.last_name.upper(), self.first_name)
        return full_name.strip()

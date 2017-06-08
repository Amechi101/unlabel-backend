from django.db import models
from oscar.apps.address.models import Country
import boto3
from oscar.apps.customer.abstract_models import AbstractUser


class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    sex_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    ucc_handle = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    is_influencer = models.BooleanField(default=False)
    is_brand = models.BooleanField(default=False)
    gender = models.CharField(choices=sex_choice, max_length=1, null=True, blank=True)
    image = models.ImageField(upload_to='Influencers', null=True, blank=True)
    influencer_industry = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )
    country = models.ForeignKey(Country, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    def get_full_name(self):
        full_name = '%s %s' % (self.last_name.upper(), self.first_name)
        return full_name.strip()

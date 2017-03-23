from oscar.apps.offer.abstract_models import AbstractConditionalOffer, AbstractRange
from django.db import models
from oscarapps.partner.models import Partner

class ConditionalOffer(AbstractConditionalOffer):
    brand = models.ForeignKey(Partner, blank=True, null=True, verbose_name="Brand")



class Range(AbstractRange):
    brand = models.ForeignKey(Partner, blank=True, null=True, verbose_name="Brand")


from oscar.apps.offer.models import *  # noqa

from oscar.apps.customer.models import *
from oscar.apps.customer.abstract_models import *
from django.contrib.auth.models import User
from oscar.apps.customer.abstract_models import AbstractUser
from django.db import models
from oscarapps.catalogue.models import *
from django.utils.translation import gettext as _


class UserProductLike(models.Model):
    user = models.ForeignKey( User )
    product_like = models.ForeignKey( 'catalogue.Product' )

    class Meta:
        verbose_name = _('Product_Like')
        verbose_name_plural = _('Product_Likes')

    def __str__(self):
        return self.product_like.likes


from oscar.apps.customer.models import *
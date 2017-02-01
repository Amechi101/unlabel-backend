# from oscar.apps.customer.abstract_models import AbstractUser
from django.db import models
# from oscarapps.catalogue.models import *
from django.utils.translation import gettext as _
from django.conf import settings



class UserProductLike(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL )
    product_like = models.ForeignKey( 'catalogue.Product' )

    class Meta:
        verbose_name = _('Product_Like')
        verbose_name_plural = _('Product_Likes')

    def __str__(self):
        return self.product_like.likes

class UserVerify(models.Model):
    customer = models.ForeignKey( settings.AUTH_USER_MODEL )
    verification_code = models.TextField(null=False,blank=False, max_length=11)
    created_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = ('User Verification')

    def __str__(self):
        return self.customer.email



from oscar.apps.customer.models import *
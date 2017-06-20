# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import random
import string
from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail.message import EmailMessage
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models.signals import pre_save

from oscarapps.address.models import Locations
from oscarapps.catalogue.models import Product
from users.models import User
from push_notification.models import APNSDevice,NotificationDetails, SNS
from oscarapps.partner.models import Style, StockRecord


class BaseApplicationModel(models.Model):
    """
    An abstract base class model that common attributes
    """
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'influencers'
        abstract = True


class Influencers(BaseApplicationModel):
    """
    Information for each influencer
    """
    auto_id = models.CharField(unique=True, max_length=16, blank=True, null=True, default="",
                               verbose_name=_('Influencer ID'))
    bio = models.TextField(blank=True, default="", verbose_name=_('Bio'))
    location = models.ForeignKey(Locations, models.SET_NULL, null=True, blank=True, default="",
                                 verbose_name=_('Location'),related_name="influencer_location")
    users = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="influencers", blank=True,
                                 verbose_name=_("Users"))
    height = models.PositiveIntegerField(default=0, verbose_name=_('Height'), help_text=_('US Measurements'))
    chest_or_bust = models.PositiveIntegerField(default=0, verbose_name=_('Chest or Bust'),
                                                help_text=_('US Measurements'))
    hips = models.PositiveIntegerField(default=0, verbose_name=_('hips'), help_text=_('US Measurements'))
    waist = models.PositiveIntegerField(default=0, verbose_name=_('waist'), help_text=_('US Measurements'))
    styles = models.ManyToManyField(Style, null=True, blank=True)

    def id_generator(self, size=10, chars=string.ascii_uppercase + string.digits):
        auto_id = ''.join(random.choice(chars) for _ in range(size))
        if auto_id not in Influencers.objects.values_list('auto_id', flat=True):
            return auto_id
        else:
            self.id_generator()

    def save(self, *args, **kwargs):
        super(Influencers, self).save(*args, **kwargs)
        if not self.auto_id:
            self.auto_id = self.id_generator()
            self.save()

    def __str__(self):

        return self.users.first_name


class InfluencerInvite(models.Model):
    email = models.EmailField(blank=True, null=True)
    code = models.CharField(max_length=20, blank=False, null=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class InfluencerProductReserve(models.Model):
    influencer = models.ForeignKey(Influencers, blank=False, null=False, verbose_name=_('Influencer'))
    product = models.ForeignKey(Product, blank=False, null=False, verbose_name=_('Product'))
    date_reserved = models.DateTimeField(null=False, blank=False, verbose_name=_('Product Reserved Date'))
    date_rented = models.DateTimeField(null=True, blank=True, verbose_name=_('Product Rented Date'))
    date_live = models.DateTimeField(null=True, blank=True, verbose_name=_('Product Live Date'))
    date_picked = models.DateTimeField(null=True, blank=True, verbose_name=_('Product Picked Date'))
    date_return = models.DateTimeField(null=True, blank=True, verbose_name=_('Product Return Date'))
    is_live = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _('Influencer Product Reservations')

    def __str__(self):
        return self.influencer.users.email + "-->" + self.product.title

    def get_product_rental_status(self):
        rental_status = {'NON':"None",'REN':'Rented','RET':'Returned','U':'Unreserved','R':'Reserved' }
        if self.product.structure == 'child':
            product = self.product.parent
            return rental_status[product.rental_status]
        else:
            return rental_status[self.product.rental_status]





class InfluencerProductUnreserve(models.Model):

    self = 'SELF'
    sys = 'SYS'
    type_choices = ((self, 'SELF'),
                    (sys, 'SYS'))
    influencer = models.ForeignKey(Influencers, blank=False, null=False, verbose_name=_('Influencer'))
    product = models.ForeignKey(Product, blank=False, null=False, verbose_name=_('Product'))
    date_unreserved = models.DateTimeField(auto_now_add=True, verbose_name=_('Product Reserved Date'))
    type = models.TextField(choices=type_choices, null=False, blank=False)

    class Meta:
        verbose_name_plural = _('Influencer Product-Unreserve')


@receiver(pre_save, sender=Product, dispatch_uid="update_rental_date")
def update_influencer_product_rental_info(sender, instance, **kwargs):
    try:
        current_obj = Product.objects.get(pk=instance.pk)
        if current_obj.structure == 'parent':
            child_products = Product.objects.filter(parent=current_obj)
            for child in child_products:
                try:
                    influencer_product_reserve = InfluencerProductReserve.objects.get(product=child)
                    influencer_user = Influencers.objects.get(pk=influencer_product_reserve.influencer.id)
                    if instance.rental_status == "REN" and current_obj.rental_status == "R":
                        child.rental_status = "REN"
                        child.save()
                        influencer_product_reserve.date_rented = datetime.now()
                        influencer_product_reserve.save()
                        notification = NotificationDetails()
                        notification.notification_type = 'pr'
                        notification.payload = json.dumps({'type': 'pr', 'product_id': current_obj.pk})
                        notification.sent = False
                        notification.text = "You have rented " + str(current_obj.title) + "."
                        notification.user = influencer_user.users
                        notification.save()
                except:
                    print("-->error in signal--> changing status of parent")
        elif current_obj.structure == 'standalone':
            try:
                influencer_product_reserve = InfluencerProductReserve.objects.get(product=current_obj)
                influencer_user = Influencers.objects.get(pk=influencer_product_reserve.influencer)
                if instance.rental_status == "REN" and current_obj.rental_status == "R":
                    influencer_product_reserve.date_rented = datetime.now()
                    influencer_product_reserve.save()
                    notification = NotificationDetails()
                    notification.notification_type = 'pr'
                    notification.payload=json.dumps({'type': 'pr', 'product_id': current_obj.pk})
                    notification.sent = False
                    notification.text = "You have rented " + str(current_obj.title) + "."
                    notification.user = influencer_user.users
                    notification.save()
                # if instance.rental_status == "RET" and current_obj.rental_status == "REN":
                #     current_obj.rental_status='RET'
                #     product_to_return = Product.objects.get(product=current_obj)
                #     self.send_email_for_reserved_product(product_to_return, influencer_user.users)
                #     current_obj.save()
            except:
                print("-->error in signal--> changing status of standalone")
    except:
        pass


def send_email_for_reserved_product(self, product_to_return, influencer_user):
        """
            Send email when product is returned
        """
        stock_brand = StockRecord.objects.filter(product=product_to_return)[0].partner  # partner name
        brand_user = stock_brand.users.all()[0]  # partner's mail id
        self.mail_send(brand_user)  # send mail to partner
        self.mail_send(influencer_user.users)  # send mail to influencer


def mail_send(self, to_mail):
    """
        Send mail to a recipient
    """
    mailid = to_mail
    email = EmailMessage()
    email.subject = "Product Returned"
    email.content_subtype = "html"
    email.body = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><META http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
                    <body>
                    <h2>Welcome to unlabel</h2>
                    <p style = 'font-size:14px;'>Hello,</p>
                    <p>Product has been returned.<br/>
                    </p>
                    <br/>
                    <br/>
                    Thank you!<br/><br/>
                    <p style='font-size:11px;'><i>*** This is a system generated email; Please do not reply. ***</i></p>
                    </body>
                    </head>
                    </html>"""
    email.from_email = "Unlabel App"
    email.to = [mailid]
    email.send()


pre_save.connect(update_influencer_product_rental_info, sender=Product, dispatch_uid="update_rental_date")



from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractCategory, AbstractProductImage
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from oscarapps.partner.models import Partner
from oscarapps.influencers.models import *


class BaseApplicationModel(models.Model):
    """
    An abstract base class model that common attributes
    """
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        app_label = 'Catalogue'
        abstract = True


class InfluencerProductImage(models.Model):

    product = models.ForeignKey(
        'catalogue.Product', related_name='influencer_product_images', verbose_name=_("Product"))
    original = models.ImageField(
        _("Original"), upload_to=settings.OSCAR_IMAGE_FOLDER, max_length=255)
    caption = models.CharField(_("Caption"), max_length=200, blank=True)

    #: Use display_order to determine which is the "primary" image
    display_order = models.PositiveIntegerField(
        _("Display order"), default=0,
        help_text=_("An image with a display order of zero will be the primary"
                    " image for a product"))
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)

    class Meta:
        app_label = 'catalogue'
        # Any custom models should ensure that this ordering is unchanged, or
        # your query count will explode. See AbstractProduct.primary_image.
        ordering = ["display_order"]
        unique_together = ("product", "display_order")
        verbose_name = _('Influencer product image')
        verbose_name_plural = _('influencer product images')

    def __str__(self):
        return u"Influencer image of '%s'" % self.product

    def is_primary(self):
        """
        Return bool if image display order is 0
        """
        return self.display_order == 0

    def delete(self, *args, **kwargs):
        """
        Always keep the display_order as consecutive integers. This avoids
        issue #855.
        """
        super(InfluencerProductImage, self).delete(*args, **kwargs)
        for idx, image in enumerate(self.product.influencer_product_images.all()):
            image.display_order = idx
            image.save()


class Product(AbstractProduct, BaseApplicationModel):
    MALE = 'M'
    FEMALE = 'F'
    UNISEX = 'U'
    item_sex_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNISEX, 'Unisex'),
    )

    UNRESERVED = 'U'
    RESERVED = 'R'
    DRAFT = 'D'
    LIVE = 'L'
    status_choice = (
        (UNRESERVED, 'Unreserved'),
        (RESERVED, 'Reserved'),
        (DRAFT, 'Draft'),
        (LIVE, 'Live')
    )

    NONE = "NON"
    RENTED = 'REN'
    RETURNED = 'RET'
    rental_status_choice = (
        (NONE, 'None'),
        (RENTED, 'Rented'),
        (RETURNED, 'Returned'),
    )

    YES = 'Y'
    NO = 'N'
    shipping_choice = (
        (YES, 'Yes'),
        (NO, 'No'),
    )
    brand = models.ForeignKey(Partner, blank=True, null=True, default="", verbose_name="Brand")
    material_info = models.TextField(blank=True, default="", verbose_name=_('Material & Care Information'))
    likes = models.PositiveIntegerField(default=0)
    influencer_description = models.TextField(max_length=200, blank=True, null=True,
                                              verbose_name=_('Influencer Product Description'))
    weight = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Product weight information'))
    on_sale = models.BooleanField(default=True, verbose_name=_('Product on sale'))
    item_sex_type = models.CharField(
        max_length=1,
        choices=item_sex_choice,
        default=UNISEX,
    )
    status = models.CharField(
        max_length=1,
        choices=status_choice,
        default=UNRESERVED,
        verbose_name=_("Status")
    )
    rental_status = models.CharField(
        max_length=3,
        choices=rental_status_choice,
        default=NONE,
        verbose_name=_("Rental Status")
    )
    requires_shipping = models.CharField(
        max_length=1,
        choices=shipping_choice,
        default=YES,
        verbose_name=_('Requires shipping.?')
    )

    # Metadata
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return "{0}".format(self.title)

    def save(self, *args, **kwargs):
        if self.description:
            self.description = strip_tags(self.description)
        if self.material_info:
            self.material_info = strip_tags(self.material_info)
        if self.influencer_description:
            self.influencer_description = strip_tags(self.influencer_description)
        super(Product, self).save(*args, **kwargs)



from oscar.apps.catalogue.models import *
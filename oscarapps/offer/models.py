from django.db import models
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_class, get_model
from oscar.apps.offer.abstract_models import AbstractConditionalOffer, AbstractRange, AbstractBenefit

from oscarapps.partner.models import Partner

class ConditionalOffer(AbstractConditionalOffer):
    brand = models.ForeignKey(Partner, blank=True, null=True, verbose_name="Brand")

    def products(self):
        """
        Return a queryset of products in this offer
        """
        Product = get_model('catalogue', 'Product')
        if not self.has_products:
            return Product.objects.none()

        cond_range = self.condition.range
        if cond_range.includes_all_products:
            # Return ALL the products
            queryset = Product.browsable
        else:
            queryset = cond_range.all_products()
        if self.brand:
            return queryset.filter(is_discountable=True, brand=self.brand).exclude(
            structure=Product.CHILD)
        return queryset.filter(is_discountable=True).exclude(
            structure=Product.CHILD)


class Range(AbstractRange):
    brand = models.ForeignKey(Partner, blank=True, null=True, verbose_name="Brand")

    def contains_product(self, product):  # noqa (too complex (12))
        """
        Check whether the passed product is part of this range.
        """
        # Delegate to a proxy class if one is provided
        if self.proxy:
            return self.proxy.contains_product(product)

        excluded_product_ids = self._excluded_product_ids()
        if product.id in excluded_product_ids:
            if self.brand:
                if product.brand == self.brand:
                    return True
                return False
            return False
        ####################
        if self.includes_all_products:
            if self.brand:
                   if product.brand == self.brand:
                       return True
                   return False
            return True
        ######################
        if product.get_product_class().id in self._class_ids():
            if self.brand:
                if product.brand == self.brand:
                    return True
                return False
            return True
        included_product_ids = self._included_product_ids()
        # If the product's parent is in the range, the child is automatically included as well
        if product.is_child and product.parent.id in included_product_ids:
            if self.brand:
                if product.brand == self.brand:
                    return True
                return False
            return True
        if product.id in included_product_ids:
            return True
        test_categories = self.included_categories.all()
        if test_categories:
            for category in product.get_categories().all():
                for test_category in test_categories:
                    if category == test_category \
                            or category.is_descendant_of(test_category):
  ############################################################
                        if self.brand:
                            if product.brand == self.brand:
                                return True
                            return False
                        return True
  ############################################################
        return False





    # Shorter alias
    contains = contains_product


class Benefit(AbstractBenefit):

    def clean_percentage(self):
        if not self.value:
            raise exceptions.ValidationError(
                _("A discount value is required"))
        if not self.range:
            raise exceptions.ValidationError(
                _("Percentage benefits require a product range"))
        if self.value > 100:
            raise exceptions.ValidationError(
                _("Percentage discount cannot be greater than 100"))

    def clean_shipping_percentage(self):
        if not self.value:
            raise exceptions.ValidationError(
                _("A discount value is required"))
        if self.value > 100:
            raise exceptions.ValidationError(
                _("Percentage discount cannot be greater than 100"))
        if self.range:
            raise exceptions.ValidationError(
                _("No range should be selected as this benefit does not "
                  "apply to products"))
        if self.max_affected_items:
            raise exceptions.ValidationError(
                _("Shipping discounts don't require a 'max affected items' "
                  "attribute"))

from oscar.apps.offer.models import *  # noqa

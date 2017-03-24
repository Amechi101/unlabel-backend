from oscar.apps.offer.abstract_models import AbstractConditionalOffer, AbstractRange
from django.db import models
from oscarapps.partner.models import Partner

class ConditionalOffer(AbstractConditionalOffer):
    brand = models.ForeignKey(Partner, blank=True, null=True, verbose_name="Brand")


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
            return False
        ####################
        if self.includes_all_products:
            print(self.brand, product.brand)
            if self.brand:
                   if product.brand == self.brand:

                       return True
                   return False
            return True
        ######################
        if product.get_product_class().id in self._class_ids():
            return True
        included_product_ids = self._included_product_ids()
        # If the product's parent is in the range, the child is automatically included as well
        if product.is_child and product.parent.id in included_product_ids:
            return True
        if product.id in included_product_ids:
            return True
        test_categories = self.included_categories.all()
        if test_categories:
            for category in product.get_categories().all():
                for test_category in test_categories:
                    if category == test_category \
                            or category.is_descendant_of(test_category):
                        return True
        return False

    # Shorter alias
    contains = contains_product

from oscar.apps.offer.models import *  # noqa

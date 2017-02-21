from django_tables2 import A, Column, LinkColumn, TemplateColumn
from django.utils.translation import ugettext_lazy as _
from oscar.apps.dashboard.catalogue.tables import ProductTable as CoreProductTable
from oscar.apps.dashboard.catalogue.tables import *


class ProductTable(CoreProductTable):
    brand = TemplateColumn(
        verbose_name=_('Brand'),
        template_name='dashboard/catalogue/product_brand.html',
        order_by='brand', accessor=A('brand'))

    class Meta(CoreProductTable.Meta):
        sequence = ('title', 'upc', 'brand', 'image', 'product_class', 'variants',
                    'stock_records', '...', 'date_updated', 'actions')
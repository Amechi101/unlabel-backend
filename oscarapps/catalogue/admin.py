from django.contrib import admin
from oscarapps.catalogue.models import InfluencerProductImage

admin.site.register(InfluencerProductImage)
from oscar.apps.catalogue.admin import *  # noqa

from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class ProductResource(resources.ModelResource):

    class Meta:
        model = Product


class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    date_hierarchy = 'date_created'
    list_display = ('get_title', 'upc', 'get_product_class', 'structure',
                    'attribute_summary', 'date_created')
    list_filter = ['structure', 'is_discountable']
    raw_id_fields = ['parent']
    inlines = [AttributeInline, CategoryInline, ProductRecommendationInline]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['upc', 'title']


    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        return (
            qs
            .select_related('product_class', 'parent')
            .prefetch_related(
                'attribute_values',
                'attribute_values__attribute'))

admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)

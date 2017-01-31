from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from applications.models import Brand, Product, City, Location, Style, Category

def brand_active(modeladmin, request, queryset):
	queryset.update(brand_isActive=True)

def brand_not_active(modeladmin, request, queryset):
	queryset.update(brand_isActive=False)

brand_active.short_description = "Brand is active"
brand_not_active.short_description = "Brand is not active"

class BrandAdmin(admin.ModelAdmin):
	"""
	This admin display is for Superusers Only
	"""
	list_display = ["brand_name", "menswear", "womenswear", "categories", "styles", "brand_isActive", "brand_city", "brand_description"]

	ordering = ['brand_name']
	
	list_filter = ['brand_isActive','created','modified']
	
	fieldsets = [
        ("General Information", {
            'fields': ("brand_name", "brand_description", "brand_feature_image", "brand_website_url")
        }),
        ("Location", {
            'fields': ( "brand_city",)
        }),
        ("Sex", {
            'fields': ("menswear", "womenswear")
        }),
        ("Category", {
            'fields': ("brand_category",)
        }),
        ("Style", {
            'fields': ("brand_style",)
        }),
        ("Activation", {
            'fields': ("brand_isActive",)
        })
    ]
	
	search_fields = ["brand_name"]
	
	list_per_page = 20	
	
	actions = [ brand_active, brand_not_active ]

	def categories(self, obj):
		return ",\n".join([c.name for c in obj.brand_category.all()])

	def styles(self, obj):
		return ",\n".join([s.name for s in obj.brand_style.all()])

class CategoryAdmin(admin.ModelAdmin):
	"""
	This admin display is for Superusers Only
	"""
	list_display = ["name","description"]

	ordering = ['name']
	
	search_fields = ["name"]
	
	list_per_page = 20	

class StyleAdmin(admin.ModelAdmin):
	"""
	This admin display is for Superusers Only
	"""
	list_display = ["name","description"]

	ordering = ['name']
	
	search_fields = ["name"]
	
	list_per_page = 20	

class CityAdmin(admin.ModelAdmin):
	"""
	This admin display is for Superusers Only
	"""
	list_display = ["city", "location"]

	ordering = ["city"]

	search_fields = ["city"]
	
	list_per_page = 20	

class LocationAdmin(admin.ModelAdmin):
	"""
	This admin display is for Superusers Only
	"""
	list_display = ["state_or_country", "location_choices"]

	ordering = ["state_or_country"]

	search_fields = ["state_or_country"]
	
	list_per_page = 20	

class ProductAdmin(admin.ModelAdmin):
	"""
	This admin display is for Superusers & Staff Members
	"""
	list_display = ["brand", "product_name", "product_price", "product_currency", "product_isActive"]

	list_filter = ['product_isActive',]

	fieldsets = [
        ("General Information", {
            'fields': ( "product_name", "product_price", "product_currency", "product_url", "product_image", "product_isActive"),
        }),
        ("Select Related Brand", {
            'fields': ("brand",),
        })
    ]
	
	search_fields = ["brand__brand_name"]
	list_per_page = 20	
	
	# class method Functions
	def get_queryset(self, request):
		qs = super(ProductAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(brand__brand_owner=request.user)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "brand" and not request.user.is_superuser:
			kwargs["queryset"] = Brand.objects.filter(brand_owner=request.user)
			return db_field.formfield(**kwargs)
		return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


# Register Models below
admin.site.register(Brand, BrandAdmin)
admin.site.register(Style, StyleAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(City, CityAdmin)
# admin.site.register(Location, LocationAdmin)








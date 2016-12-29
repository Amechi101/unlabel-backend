from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from influencers.models import Influencers
# from influencers.models import Influencers, City, StateCountry


# class InfluencersAdmin(admin.ModelAdmin):
# 	"""
# 	This admin display is for Superusers Only
# 	"""
# 	list_display = ["name", "hometown", "instagram_handle", "influencer_isActive", "slug"]
#
# 	fieldsets = [
#         ("General Information", {
#             'fields': ("name", "hometown", "instagram_handle","bio","style_Preference", "instagram_url", "website_url", "website_name", "website_isActive",
#              "image", "photographer_credit", "photographer_credit_isActive")
#         }),
#         ("Brand Information", {
#             'fields': ("brands", "question_brand_attraction",)
#         }),
#         ("Product Information", {
#             'fields': ("question_product_favorite_name", "question_product_favorite_explanation", "question_product_favorite_url",
#             	"question_product_favorite_product_pairing" )
#         }),
#         ("Style Question", {
#             'fields': ("question_personal_style_one",)
#         }),
#         ("Other Questions", {
#             'fields': ("question_fashion_advice", "question_favorite_season")
#         }),
#         ("Activation", {
#             'fields': ("influencer_isActive",)
#         })
#     ]
#
# 	search_fields = ["name"]
#
#
# class CityAdmin(admin.ModelAdmin):
# 	"""
# 	This admin display is for Superusers Only
# 	"""
# 	list_display = ["city", "state_or_country"]
#
# 	ordering = ["city"]
#
# 	search_fields = ["city"]
#
# 	list_per_page = 20
#
# class StateCountryAdmin(admin.ModelAdmin):
# 	"""
# 	This admin display is for Superusers Only
# 	"""
# 	list_display = ["name", "location_choice"]
#
# 	ordering = ["name"]
#
# 	search_fields = ["name"]
#
# 	list_per_page = 20
#
#
# # Register Models below
# admin.site.register(Influencers, InfluencersAdmin)
# admin.site.register(City, CityAdmin)
# admin.site.register(StateCountry, StateCountryAdmin)
admin.site.register(Influencers)








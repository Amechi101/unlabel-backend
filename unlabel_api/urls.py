from django.conf.urls import include, url

from tastypie.api import Api

from unlabel_api.brands_api._prod_api import LabelResource, LocationResource, CategoryResource, StyleResource

version_num_api_prod_labels = Api(api_name='v3')
version_num_api_prod_styles = Api(api_name='v3')
version_num_api_prod_categories = Api(api_name='v3')
version_num_api_prod_locations = Api(api_name='v3')

version_num_api_prod_labels.register( LabelResource() )
version_num_api_prod_locations.register( LocationResource() )
version_num_api_prod_categories.register( CategoryResource() )
version_num_api_prod_styles.register( StyleResource() )

urlpatterns = [
	
	# api's
	url(r'^labels-api/', include(version_num_api_prod_labels.urls) ) ,
	url(r'^locations-api/', include(version_num_api_prod_locations.urls) ) ,
	url(r'^categories-api/', include(version_num_api_prod_categories.urls) ) ,
	url(r'^styles-api/', include(version_num_api_prod_styles.urls) ) ,	
]

###################### dev #################################
# from applications.api._dev_api import DevLabelResource, DevLocationResource

# version_num_api_dev = Api(api_name='v3')
# version_num_api_dev.register( DevLabelResource() )
# version_num_api_dev.register( DevLocationResource() )

# urlpatterns = [
# 	url(r'^labels-api/', include(version_num_api_dev.urls) ) ,
# 	url(r'^locations-api/', include(version_num_api_dev.urls) ) ,
# ]


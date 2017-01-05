from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import Q

from tastypie.resources import ModelResource

from tastypie.paginator import Paginator
from tastypie import fields

from tastypie.authentication import Authentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from applications.models import Brand, Product, Location, City

import cloudinary.api


class DevUserAuthentication(Authentication):
	def is_authenticated(self, request, **kwargs):
		if request.user.is_superuser:
			return True
		else:
			return False

	# Optional but recommended
	def get_identifier(self, request):
		return request.user.username

class DevLocationResource(ModelResource):

	class Meta:
		excludes = ['modified', 'id', 'created']

		queryset = Location.objects.all()

		include_resource_uri = False

		resource_name = 'Devlocations'

		limit = 0

		max_limit = 0

		filtering =  {
			"location_choices": ALL
		}

	def alter_list_data_to_serialize(self, request, data):
		data['locations'] = data['objects']
		
		del data['objects']
		
		return data

class DevCityResource(ModelResource):

	location = fields.ForeignKey(DevLocationResource, 'location', full=True)

	class Meta:
		excludes = ['modified', 'id', 'created']

		queryset = City.objects.all()

		include_resource_uri = False

		resource_name = 'Devcity'

		filtering =  {
			"city": ALL,
			"location": ALL_WITH_RELATIONS
		}

	def dehydrate(self, bundle):

		bundle.data['location'] = bundle.data['location'].data['state_or_country']
		
		return bundle

class DevLabelResource(ModelResource):

	brand_city = fields.ForeignKey(DevCityResource, 'brand_city', full=True)
	
	class Meta:

		filtering = {
			"id": ALL,
			"menswear": ALL,
			"womenswear":ALL,
			"brand_category": ALL,
			"brand_city": ALL_WITH_RELATIONS,
			"location": ['exact', 'startswith', 'endswith', 'contains'],
		}

		queryset = Brand.objects.all().order_by('-created')
		
		resource_name = 'Devlabels'
		
		include_resource_uri = False

		limit = 10

		excludes = ['modified']

		paginator_class = Paginator

		authentication = MultiAuthentication( DevUserAuthentication(), ApiKeyAuthentication() )


	# def dehydrate(self, bundle):

	# 	image = bundle.data['brand_feature_image']
	# 	if image:

	# 		image = cloudinary.api.resource( image )['secure_url']
			
	# 		bundle.data['brand_feature_image'] = image
			
	# 		return bundle

	def build_filters(self, filters=None):
		if filters is None:
			filters = {}

		orm_filters = super(DevLabelResource, self).build_filters(filters)

		if('location' in filters):
			query = filters['location']
			
			qset = (
				Q(brand_city__location__state_or_country__exact=query) 
			)
			
			orm_filters.update({'custom': qset})

		return orm_filters

	def apply_filters(self, request, applicable_filters):
		if 'custom' in applicable_filters:
			custom = applicable_filters.pop('custom')

		else:
			custom = None

		semi_filtered = super(DevLabelResource, self).apply_filters(request, applicable_filters)

		return semi_filtered.filter(custom) if custom else semi_filtered

	def alter_list_data_to_serialize(self, request, data):
		data['labels'] = data['objects']
		
		del data['objects']
		
		return data


# class DevProductResource(ModelResource):

# 	brand = fields.ForeignKey(DevLabelResource, 'brand', full=True)
	
# 	class Meta:
# 		excludes = ['id', 'modified']

# 		queryset = Product.objects.all().order_by('-created')

# 		include_resource_uri = False

# 		limit = 6

# 		resource_name = 'Devproducts'

# 		filtering =  {
# 			"brand": ALL_WITH_RELATIONS,
# 			"label_id": ['exact', 'startswith', 'endswith', 'contains'],
# 		}

# 	def build_filters(self, filters=None):
# 		if filters is None:
# 			filters = {}

# 		orm_filters = super(DevProductResource, self).build_filters(filters)

# 		if('label_id' in filters):
# 			query = filters['label_id']
			
# 			qset = (
# 				Q(brand__id=query) 
# 			)
			
# 			orm_filters.update({'custom': qset})

# 		return orm_filters

# 	def apply_filters(self, request, applicable_filters):
# 		if 'custom' in applicable_filters:
# 			custom = applicable_filters.pop('custom')

# 		else:
# 			custom = None

# 		semi_filtered = super(DevProductResource, self).apply_filters(request, applicable_filters)

# 		return semi_filtered.filter(custom) if custom else semi_filtered

# 	def alter_list_data_to_serialize(self, request, data):
# 		data['products'] = data['objects']
		
# 		del data['objects']
		
# 		return data


# 	def dehydrate(self, bundle):
# 		bundle.data['brand'] = bundle.data['brand'].data['id']
# 		return bundle

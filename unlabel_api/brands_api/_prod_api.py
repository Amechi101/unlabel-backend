from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify

from tastypie.resources import ModelResource

from tastypie.paginator import Paginator
from tastypie import fields

from tastypie.authentication import Authentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from applications.models import Brand, Product, Location, City, Style, Category

class UserAuthentication(Authentication):
	def is_authenticated(self, request, **kwargs):
		if request.user.is_superuser:
			return True
		else:
			return False

	# Optional but recommended
	def get_identifier(self, request):
		return request.user.username

class LocationResource(ModelResource):

	class Meta:
		excludes = ['modified', 'id', 'created']

		queryset = Location.objects.all()

		include_resource_uri = False

		resource_name = 'locations'

		limit = 0

		max_limit = 0

		filtering =  {
			"location_choices": ALL
		}

	def alter_list_data_to_serialize(self, request, data):
		data['locations'] = data['objects']
		
		del data['objects']
		
		return data

class CityResource(ModelResource):

	location = fields.ForeignKey(LocationResource, 'location', full=True)

	class Meta:
		excludes = ['modified', 'id', 'created']

		queryset = City.objects.all()

		include_resource_uri = False

		resource_name = 'city'

		filtering =  {
			"city": ALL,
			"location": ALL_WITH_RELATIONS
		}

	def dehydrate(self, bundle):

		bundle.data['location'] = bundle.data['location'].data['state_or_country']
		
		return bundle

class CategoryResource(ModelResource):

	class Meta:
		excludes = ['modified', 'id', 'created']

		queryset = Category.objects.all()

		include_resource_uri = False

		limit = 0

		max_limit = 0

		resource_name = 'categories'

		filtering =  {
			"name": ALL
		}

	def alter_list_data_to_serialize(self, request, data):
		data['categories'] = data['objects']
		
		del data['objects']
		
		return data

class StyleResource(ModelResource):

	class Meta:
		excludes = ['modified', 'id', 'created']

		queryset = Style.objects.all()

		include_resource_uri = False

		limit = 0

		max_limit = 0

		resource_name = 'styles'

		filtering =  {
			"name": ALL
		}

	def alter_list_data_to_serialize(self, request, data):
		data['categories'] = data['objects']
		
		del data['objects']
		
		return data

class LabelResource(ModelResource):

	brand_city = fields.ForeignKey(CityResource, 'brand_city', full=True)

	brand_category = fields.ToManyField(CategoryResource, 'brand_category', full=True)

	brand_style = fields.ToManyField(StyleResource, 'brand_style', full=True)
	
	class Meta:

		filtering = {
			"id": ALL,
			"menswear": ALL,
			"womenswear":ALL,
			"brand_category": ALL_WITH_RELATIONS,
			"brand_style": ALL_WITH_RELATIONS,
			"brand_city": ALL_WITH_RELATIONS,
			"location": ['exact', 'startswith', 'endswith', 'contains'],
		}

		queryset = Brand.objects.all().order_by('brand_name').distinct()
		
		resource_name = 'labels'
		
		include_resource_uri = False

		limit = 10

		excludes = ['modified']

		paginator_class = Paginator

		authentication = MultiAuthentication( UserAuthentication(), ApiKeyAuthentication() )

	def dehydrate(self, bundle):

		categories = bundle.data['brand_category']
		styles = bundle.data['brand_style']
		
		for category, style in zip(categories, styles):

			del category.data['description']
			del style.data['description']
		
		return bundle
	
	def build_filters(self, filters=None):
		if filters is None:
			filters = {}

		orm_filters = super(LabelResource, self).build_filters(filters)


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

		semi_filtered = super(LabelResource, self).apply_filters(request, applicable_filters)

		return semi_filtered.filter(custom) if custom else semi_filtered

	def alter_list_data_to_serialize(self, request, data):
		data['labels'] = data['objects']
		
		del data['objects']
		
		return data


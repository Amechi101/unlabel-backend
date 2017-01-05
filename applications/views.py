from __future__ import unicode_literals 

from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from applications.models import Brand, Category, Style


class BrandDetailView(SingleObjectMixin, ListView):
	
	model = Brand
	
	template_name = 'brands/_brand_detail.html'
	
	def get(self, request, *args, **kwargs):
		self.object = self.get_object(queryset=Brand.objects.all())

		return super(BrandDetailView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):

		ctx = super(BrandDetailView, self).get_context_data(**kwargs)
		
		ctx['brand'] = self.object
		ctx['category_list'] = Category.objects.filter(brand=self.object)
		ctx['style_list'] = Style.objects.filter(brand=self.object)
		

		return ctx

	def get_queryset(self,  **kwargs):
		return self.object


class BrandInviteView(SingleObjectMixin, ListView):
	
	model = Brand
	
	template_name = 'brands/_brand_invite.html'
	
	def get(self, request, *args, **kwargs):
		self.object = self.get_object(queryset=Brand.objects.all())

		return super(BrandInviteView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):

		ctx = super(BrandInviteView, self).get_context_data(**kwargs)
		ctx['brand'] = self.object

		return ctx

	def get_queryset(self,  **kwargs):
		return self.object

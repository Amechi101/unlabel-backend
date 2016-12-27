from __future__ import unicode_literals 

from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView

from applications.models import Brand, Category, Style


class HomePageView(ListView):

	template_name = 'site/pages/_homepage.html'

	model = Brand

	def get_context_data(self, **kwargs):
		ctx = super(HomePageView, self).get_context_data(**kwargs)
	
		ctx['brand_list'] = Brand.objects.filter( brand_isActive=True ).order_by('brand_name')

		return ctx

class AboutView(TemplateView):

	template_name = 'site/pages/_about.html'

class LegalStuffView(TemplateView):

	template_name = 'site/pages/_terms.html'


class PrivacyPolicyView(TemplateView):
	
	template_name = 'site/pages/_privacy_policy.html'
		

class ContactView(TemplateView):
	
	template_name = 'site/pages/_contact.html'



		


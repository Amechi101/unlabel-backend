from __future__ import unicode_literals 

from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from influencers.models import Influencers

class InfluencerListView(ListView):

	template_name = 'pages/_influencers.html'

	model = Influencers

	def get_context_data(self, **kwargs):
		
		ctx = super(InfluencerListView, self).get_context_data(**kwargs)
		ctx['influencer_list'] = Influencers.objects.filter( influencer_isActive=True ).order_by('-created')

		return ctx


class InfluencerDetailView(SingleObjectMixin, ListView):
	
	model = Influencers
	
	template_name = 'pages/_influencer_detail.html'
	
	def get(self, request, *args, **kwargs):
		self.object = self.get_object(queryset=Influencers.objects.all())

		return super(InfluencerDetailView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):

		ctx = super(InfluencerDetailView, self).get_context_data(**kwargs)
		
		ctx['influencer'] = self.object
	
		return ctx

	def get_queryset(self,  **kwargs):
		return self.object

		


from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q

# class SearchView(View):
#     template_name = 'search/brands_results.html'
#     def get(self,request,*args,**kwargs):
from haystack import views

from oscar.core.loading import get_class, get_model

from oscar.apps.search import signals

Product = get_model('catalogue', 'Product')
Partner = get_model('partner','Partner')
Influencer = get_model('influencers','Influencers')
FacetMunger = get_class('search.facets', 'FacetMunger')

# class BrandFacetedSearchView(views.FacetedSearchView):
#
#     template = "search/brands_results.html"
#     search_signal = signals.user_search
#
#     def __call__(self, request):
#         response = super(BrandFacetedSearchView, self).__call__(request)
#
#         # Raise a signal for other apps to hook into for analytics
#         self.search_signal.send(
#             sender=self, session=self.request.session,
#             user=self.request.user, query=self.query)
#
#         return response
#
#     # Override this method to add the spelling suggestion to the context and to
#     # convert Haystack's default facet data into a more useful structure so we
#     # have to do less work in the template.
#     def extra_context(self):
#         extra = super(BrandFacetedSearchView, self).extra_context()
#
#         # Show suggestion no matter what.  Haystack 2.1 only shows a suggestion
#         # if there are some results, which seems a bit weird to me.
#         if self.results.query.backend.include_spelling:
#             # Note, this triggers an extra call to the search backend
#             suggestion = self.form.get_suggestion()
#             if suggestion != self.query:
#                 extra['suggestion'] = suggestion
#
#         # Convert facet data into a more useful data structure
#         if 'fields' in extra['facets']:
#             munger = FacetMunger(
#                 self.request.get_full_path(),
#                 self.form.selected_multi_facets,
#                 self.results.facet_counts())
#             extra['facet_data'] = munger.facet_data()
#             has_facets = any([len(data['results']) for
#                               data in extra['facet_data'].values()])
#             extra['has_facets'] = has_facets
#
#         # Pass list of selected facets so they can be included in the sorting
#         # form.
#         extra['selected_facets'] = self.request.GET.getlist('selected_facets')
#
#         return extra
#
#     def get_results(self):
#         # We're only interested in products (there might be other content types
#         # in the Solr index).
#         return super(BrandFacetedSearchView, self).get_results().models(Partner)
#
#
#
# class InfluencerFacetedSearchView(views.FacetedSearchView):
#
#     template = "search/influencer_results.html"
#     search_signal = signals.user_search
#
#     def __call__(self, request):
#         response = super(InfluencerFacetedSearchView, self).__call__(request)
#
#         # Raise a signal for other apps to hook into for analytics
#         self.search_signal.send(
#             sender=self, session=self.request.session,
#             user=self.request.user, query=self.query)
#
#         return response
#
#     # Override this method to add the spelling suggestion to the context and to
#     # convert Haystack's default facet data into a more useful structure so we
#     # have to do less work in the template.
#     def extra_context(self):
#         extra = super(InfluencerFacetedSearchView, self).extra_context()
#
#         # Show suggestion no matter what.  Haystack 2.1 only shows a suggestion
#         # if there are some results, which seems a bit weird to me.
#         if self.results.query.backend.include_spelling:
#             # Note, this triggers an extra call to the search backend
#             suggestion = self.form.get_suggestion()
#             if suggestion != self.query:
#                 extra['suggestion'] = suggestion
#
#         # Convert facet data into a more useful data structure
#         if 'fields' in extra['facets']:
#             munger = FacetMunger(
#                 self.request.get_full_path(),
#                 self.form.selected_multi_facets,
#                 self.results.facet_counts())
#             extra['facet_data'] = munger.facet_data()
#             has_facets = any([len(data['results']) for
#                               data in extra['facet_data'].values()])
#             extra['has_facets'] = has_facets
#
#         # Pass list of selected facets so they can be included in the sorting
#         # form.
#         extra['selected_facets'] = self.request.GET.getlist('selected_facets')
#
#         return extra
#
#     def get_results(self):
#         # We're only interested in products (there might be other content types
#         # in the Solr index).
#         return super(InfluencerFacetedSearchView, self).get_results().models(Influencer)



class BrandSearchView(View):
    template = 'search/brands_results.html'

    def get(self,request,*args,**kwargs):
        query = request.GET.get('q','')
        brands_list = Partner.objects.filter(Q(name__icontains=query)|Q(users__first_name__icontains=query))
        paginator = Paginator(brands_list, 6)
        page = request.GET.get('page')
        try:
            brands = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            brands = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            brands = paginator.page(paginator.num_pages)
        context={'brands': brands,
                 'brands_count':brands_list.count(),
                 'query':query}

        return render(request, self.template, context)


class InfluencerSearchView(View):
    template = 'search/influencer_results.html'

    def get(self,request,*args,**kwargs):
        query = request.GET.get('q','')

        influencers_list = Influencer.objects.filter(Q(users__first_name__icontains=query)|Q(users__last_name__icontains=query))
        paginator = Paginator(influencers_list, 1)
        page = request.GET.get('page')
        try:
            influencers = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            influencers = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            influencers = paginator.page(paginator.num_pages)
        context={'influencers': influencers,
                 'brands_count':influencers_list.count(),
                 'query':query}

        return render(request, self.template, context)

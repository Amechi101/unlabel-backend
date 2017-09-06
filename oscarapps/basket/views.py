from django.db.models import Q
from oscar.apps.basket.views import BasketView as CoreBasketView
from oscarapps.catalogue.models import Product



class BasketView(CoreBasketView):

    def get_context_data(self, **kwargs):
        context = super(BasketView, self).get_context_data(**kwargs)
        filtered_products = Product.objects.filter(Q(structure='parent')|Q(structure='standalone')).order_by('date_created')[:3]
        context['promoted_products'] = filtered_products

        return context
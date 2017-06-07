from oscar.apps.promotions.views import HomeView as CoreHomeView
from oscar.core.loading import get_class

from oscarapps.influencers.models import Influencers

Product = get_class('catalogue.models', 'Product')
Partner = get_class('partner.models','Partner')
ProductClass = get_class('catalogue.models', 'ProductClass')
ProductImage = get_class('catalogue.models', 'ProductImage')
ProductReview = get_class('catalogue.reviews.models', 'ProductReview')
StockRecord = get_class('partner.models', 'StockRecord')



class HomeView(CoreHomeView):
    """
    This is the home page and will typically live at /
    """
    template_name = 'promotions/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)

        available_products = []
        products = Product.objects.all().exclude(structure='child').order_by('-date_created')
        for product in products:
            info = self.request.strategy.fetch_for_parent(product)
            if info.availability.is_available_to_buy :
                available_products.append(product)
            if len(available_products) == 4:
                break
        ctx['products'] = available_products
        influencers = Influencers.objects.filter(users__is_active=True,users__is_staff=False).order_by('-users__date_joined')[:4]
        ctx['influencers'] = influencers
        brands = Partner.objects.all().order_by('-created')
        print("------------------------- ",brands)
        ctx["brands"] = brands

        ctx['user'] = self.request.user
        return ctx
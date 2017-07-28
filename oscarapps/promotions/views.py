from django.db.models import Count
from oscar.apps.promotions.views import HomeView as CoreHomeView
from oscar.core.loading import get_class

from oscarapps.influencers.models import Influencers

Product = get_class('catalogue.models', 'Product')
Partner = get_class('partner.models','Partner')
ProductClass = get_class('catalogue.models', 'ProductClass')
ProductImage = get_class('catalogue.models', 'ProductImage')
ProductReview = get_class('catalogue.reviews.models', 'ProductReview')
StockRecord = get_class('partner.models', 'StockRecord')
UserInfluencerLike = get_class('customer.models', 'UserInfluencerLike')
UserBrandLike = get_class('customer.models', 'UserBrandLike')
UserProductLike = get_class('customer.models', 'UserProductLike')





class HomeView(CoreHomeView):
    """
    This is the home page and will typically live at /
    """
    template_name = 'promotions/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)

        # available_products = []
        # products = Product.objects.all().exclude(structure='child').order_by('-date_created')
        # for product in products:
        #     info = self.request.strategy.fetch_for_parent(product)
        #     if info.availability.is_available_to_buy :
        #         available_products.append(product)
        #     if len(available_products) == 4:
        #         break

        liked_products = UserProductLike.objects.all().annotate(c=Count('product_like')).order_by('-c').values_list('product_like',flat=True)
        available_products = []
        products = Product.objects.filter(pk__in=liked_products).exclude(structure='child').order_by('-date_created')
        for product in products:
            info = self.request.strategy.fetch_for_parent(product)
            if info.availability.is_available_to_buy :
                available_products.append(product)
            if len(available_products) == 6:
                break
        if len(available_products) < 6:
            products = Product.objects.all().exclude(structure='child').order_by('-date_created')
            for product in products:
                info = self.request.strategy.fetch_for_parent(product)
                if info.availability.is_available_to_buy and product not in available_products :
                    available_products.append(product)
                if len(available_products) == 6:
                    break

        ctx['products'] = available_products

        influencer_ids = UserInfluencerLike.objects.all().annotate(c=Count('influencer')).order_by('-c').values_list('influencer',flat=True)[:4]
        if len(influencer_ids) < 4:
            influencers = Influencers.objects.filter(users__is_active=True,users__is_staff=False).order_by('-users__date_joined')[:4]
        else:
            influencers = Influencers.objects.filter(pk__in=influencer_ids)
        ctx['influencers'] = influencers

        brand_ids = UserBrandLike.objects.all().annotate(c=Count('brand')).order_by('-c').values_list('brand',flat=True)[:4]
        if len(brand_ids) < 4:
            brands = Partner.objects.all().order_by('-created')[:4]
        else:
            brands = Partner.objects.filter(pk__in=brand_ids)
        ctx["brands"] = brands

        ctx['user'] = self.request.user
        return ctx
from oscarapps.dashboard.catalogue.forms import InfluencerProductImageFormSet
from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as \
    CoreProductCreateUpdateView
from oscar.apps.dashboard.catalogue.views import *


class ProductCreateUpdateView(CoreProductCreateUpdateView):
    influencer_product_image_formset = InfluencerProductImageFormSet

    def __init__(self, *args, **kwargs):
        super(ProductCreateUpdateView, self).__init__(*args, **kwargs)
        self.formsets = {
            'category_formset': self.category_formset,
            'image_formset': self.image_formset,
            'influencer_product_image_formset': self.influencer_product_image_formset,
            'recommended_formset': self.recommendations_formset,
            'stockrecord_formset': self.stockrecord_formset}

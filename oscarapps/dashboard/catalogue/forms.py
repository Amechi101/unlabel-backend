from oscar.apps.dashboard.catalogue.forms import ProductForm as CoreProductForm

class ProductForm(CoreProductForm):
    class Meta(CoreProductForm.Meta):
        fields = [
            'title', 'upc', 'description', 'care_info_description',
            'size_and_fit_description', 'color', 'size', 'item_sex_type']
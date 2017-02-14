from django import forms
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.forms.models import inlineformset_factory

from oscar.core.loading import get_model
from oscar.forms.widgets import ImageInput
from oscar.apps.dashboard.catalogue.forms import ProductForm as CoreProductForm
from oscar.apps.dashboard.catalogue.forms import StockRecordForm as \
    CoreStockRecordForm
from oscar.apps.dashboard.catalogue.forms import ProductImageForm


Product = get_model('catalogue', 'Product')
StockRecord = get_model('partner', 'StockRecord')
InfluencerProductImage = get_model('catalogue', 'InfluencerProductImage')
ProductImage = get_model('catalogue', 'ProductImage')
SizeClass = get_model('catalogue', 'SizeClass')
Size = get_model('catalogue', 'Size')


class ProductForm(CoreProductForm):
    size_class = forms.ModelChoiceField(queryset=SizeClass.objects.all())
    size = forms.ModelMultipleChoiceField(queryset=Size.objects.all())

    class Meta(CoreProductForm.Meta):
        fields = [
            'title', 'upc', 'description', 'material_info', 'item_sex_type', 'size_class',
            'size',
            'status', 'rental_status', 'brand',
            'weight', 'on_sale', 'requires_shipping']
        labels = {
            'title': _('Name'),
        }





class StockRecordForm(CoreStockRecordForm):
    price_retail = forms.IntegerField(min_value=0)
    price_excl_tax = forms.IntegerField(min_value=0)
    cost_price = forms.IntegerField(min_value=0)

    class Meta(CoreStockRecordForm.Meta):
        fields = [
            'partner', 'partner_sku',
            'price_currency', 'price_excl_tax', 'price_retail', 'cost_price',
            'num_in_stock', 'low_stock_threshold',
        ]


BaseStockRecordFormSet = inlineformset_factory(
    Product, StockRecord, form=StockRecordForm, extra=1)


class StockRecordFormSet(BaseStockRecordFormSet):
    def __init__(self, product_class, user, *args, **kwargs):
        self.user = user
        self.require_user_stockrecord = not user.is_staff
        self.product_class = product_class

        if not user.is_staff and 'instance' in kwargs \
                and 'queryset' not in kwargs:
            kwargs.update({
                'queryset': StockRecord.objects.filter(
                    product=kwargs['instance'],
                    partner__in=user.partners.all())
            })

        super(StockRecordFormSet, self).__init__(*args, **kwargs)
        self.set_initial_data()

    def set_initial_data(self):
        """
        If user has only one partner associated, set the first
        stock record's partner to it. Can't pre-select for staff users as
        they're allowed to save a product without a stock record.
        """
        if self.require_user_stockrecord:
            try:
                user_partner = self.user.partners.get()
            except (exceptions.ObjectDoesNotExist,
                    exceptions.MultipleObjectsReturned):
                pass
            else:
                partner_field = self.forms[0].fields.get('partner', None)
                if partner_field and partner_field.initial is None:
                    partner_field.initial = user_partner

    def _construct_form(self, i, **kwargs):
        kwargs['product_class'] = self.product_class
        kwargs['user'] = self.user
        return super(StockRecordFormSet, self)._construct_form(
            i, **kwargs)

    def clean(self):
        """
        If the user isn't a staff user, this validation ensures that at least
        one stock record's partner is associated with a users partners.
        """
        if any(self.errors):
            return
        if self.require_user_stockrecord:
            stockrecord_partners = set([form.cleaned_data.get('partner', None)
                                        for form in self.forms])
            user_partners = set(self.user.partners.all())
            if not user_partners & stockrecord_partners:
                raise exceptions.ValidationError(
                    _("At least one stock record must be set to a partner that"
                      " you're associated with."))


BaseProductImageFormSet = inlineformset_factory(
    Product, ProductImage, form=ProductImageForm, extra=5)


class ProductImageFormSet(BaseProductImageFormSet):
    def __init__(self, product_class, user, *args, **kwargs):
        super(ProductImageFormSet, self).__init__(*args, **kwargs)


class InfluencerProductImageForm(forms.ModelForm):
    class Meta:
        model = InfluencerProductImage
        fields = ['product', 'original', 'caption']
        # use ImageInput widget to create HTML displaying the
        # actual uploaded image and providing the upload dialog
        # when clicking on the actual image.
        widgets = {
            'original': ImageInput(),
        }

    def save(self, *args, **kwargs):
        # We infer the display order of the image based on the order of the
        # image fields within the formset.
        kwargs['commit'] = False
        obj = super(InfluencerProductImageForm, self).save(*args, **kwargs)
        obj.display_order = self.get_display_order()
        obj.save()
        return obj

    def get_display_order(self):
        return self.prefix.split('-').pop()


BaseInfluencerProductImageFormSet = inlineformset_factory(
    Product, InfluencerProductImage, form=InfluencerProductImageForm, extra=5)


class InfluencerProductImageFormSet(BaseInfluencerProductImageFormSet):
    def __init__(self, product_class, user, *args, **kwargs):
        super(InfluencerProductImageFormSet, self).__init__(*args, **kwargs)

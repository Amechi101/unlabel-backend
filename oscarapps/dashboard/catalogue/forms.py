from django import forms
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.forms.models import inlineformset_factory
from oscar.core.utils import slugify

from oscar.core.loading import get_model
from oscar.forms.widgets import ImageInput
from oscar.apps.dashboard.catalogue.forms import ProductForm as CoreProductForm
from oscar.apps.dashboard.catalogue.forms import StockRecordForm as \
    CoreStockRecordForm
from oscar.apps.dashboard.catalogue.forms import ProductImageForm


Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')
ProductAttribute = get_model('catalogue', 'ProductAttribute')
AttributeOptionGroup = get_model('catalogue', 'AttributeOptionGroup')
Partner = get_model('partner', 'Partner')
StockRecord = get_model('partner', 'StockRecord')
InfluencerProductImage = get_model('catalogue', 'InfluencerProductImage')
ProductImage = get_model('catalogue', 'ProductImage')
SizeClass = get_model('catalogue', 'SizeClass')
Size = get_model('catalogue', 'Size')


class ProductForm(CoreProductForm):
    # size_class = forms.ModelChoiceField(queryset=SizeClass.objects.all())
    # size = forms.ModelMultipleChoiceField(queryset=Size.objects.all())

    def __init__(self, user, *args, **kwargs):
        # The user kwarg is not used by stock StockRecordForm. We pass it
        # anyway in case one wishes to customise the partner queryset
        self.user = user
        super(ProductForm, self).__init__(*args, **kwargs)

        # Restrict accessible partners for non-staff users
        if not self.user.is_staff:
            self.fields['brand'].queryset = self.user.partners.all()
            UNRESERVED = 'U'
            RESERVED = 'R'
            DRAFT = 'D'
            status_choice = (
               (UNRESERVED, 'Unreserved'),
               (RESERVED, 'Reserved'),
               (DRAFT, 'Draft'),
                )
            self.fields['status'].choices = status_choice
            self.fields['brand'].initial = Partner.objects.get(users=self.user)
            self.fields['brand'].widget = forms.HiddenInput()

        if self.instance.structure == 'parent':
            self.fields["rental_status"].widget = forms.HiddenInput()

    class Meta(CoreProductForm.Meta):
        fields = [
            'title', 'upc', 'description', 'material_info', 'item_sex_type',
            'status', 'rental_status', 'brand',
            'weight', 'on_sale', 'requires_shipping']
        labels = {
            'title': _('Name'),
        }


class StockRecordForm(forms.ModelForm):
    price_retail = forms.IntegerField(min_value=0)
    price_excl_tax = forms.IntegerField(min_value=0)
    cost_price = forms.IntegerField(min_value=0)
    def __init__(self, product_class, user, *args, **kwargs):
        # The user kwarg is not used by stock StockRecordForm. We pass it
        # anyway in case one wishes to customise the partner queryset
        self.user = user
        super(StockRecordForm, self).__init__(*args, **kwargs)

        # Restrict accessible partners for non-staff users
        if not self.user.is_staff:
            self.fields['partner'].queryset = self.user.partners.all()
            self.fields['partner'].initial = Partner.objects.get(users=self.user)
            self.fields['partner'].widget = forms.HiddenInput()

        # If not tracking stock, we hide the fields
        if not product_class.track_stock:
            for field_name in ['num_in_stock', 'low_stock_treshold']:
                if field_name in self.fields:
                    del self.fields[field_name]
        else:
            for field_name in ['price_excl_tax', 'num_in_stock']:
                if field_name in self.fields:
                    self.fields[field_name].required = True

    class Meta:
        model = StockRecord
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
        if not user.is_staff and \
           'instance' in kwargs and \
           'queryset' not in kwargs:
            kwargs.update({
                'queryset': StockRecord.objects.filter(product=kwargs['instance'],
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

    # check is parent in if to avoid validation for parent product
    # def clean(self):
    #     super(StockRecordFormSet, self).clean()
    #     if not self.user.is_staff:
    #         for form in self.forms:
    #             data = form.cleaned_data
    #             if data.get('price_excl_tax') is None:
    #                 raise forms.ValidationError("Please enter data ")
    #             return data


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


class ProductClassForm(forms.ModelForm):

    class Meta:
        model = ProductClass
        fields = ['name', 'requires_shipping', 'track_stock', 'options']


class ProductAttributesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductAttributesForm, self).__init__(*args, **kwargs)

        # because we'll allow submission of the form with blank
        # codes so that we can generate them.
        self.fields["code"].required = True

    def clean_code(self):
        code = self.cleaned_data.get("code")
        title = self.cleaned_data.get("name")

        if not code and title:
            code = slugify(title)

        return code

    def clean(self):
        cleaned_data = super(ProductAttributesForm, self).clean()
        if cleaned_data.get("type") == "option":
            if not cleaned_data.get("option_group"):
                raise forms.ValidationError("Please choose an option group")
        return cleaned_data


    class Meta:
        model = ProductAttribute
        fields = ["name", "code", "type", "option_group", "required"]

ProductAttributesFormSet = inlineformset_factory(ProductClass,
                                                 ProductAttribute,
                                                 form=ProductAttributesForm,
                                                 extra=3)

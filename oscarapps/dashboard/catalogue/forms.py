from oscar.apps.dashboard.catalogue.forms import ProductForm as CoreProductForm

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from oscar.core.loading import get_model

Style = get_model('partner', 'Style')


class ProductForm(CoreProductForm):
    class Meta(CoreProductForm.Meta):
        fields = [
            'title', 'upc', 'description', 'care_info_description',
            'size_and_fit_description', 'color', 'size', 'item_sex_type']


class StyleSearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"Style's name", u"Name"))


class StyleCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StyleCreateForm, self).__init__(*args, **kwargs)
        # Partner.name is optional and that is okay. But if creating through
        # the dashboard, it seems sensible to enforce as it's the only field
        # in the form.
        self.fields['name'].required = True

    class Meta:
        model = Style
        fields = ('name', 'description')

# ROLE_CHOICES = (
#     ('staff', _('Full dashboard access')),
#     ('limited', _('Limited dashboard access')),
# )

from oscar.apps.dashboard.partners.forms import PartnerCreateForm as CorePartnerCreateForm
from oscar.apps.dashboard.partners.forms import NewUserForm as CoreNewUserForm
from oscar.apps.dashboard.partners.forms import ExistingUserForm as CoreExistingUserForm
from oscar.apps.dashboard.partners.forms import PartnerAddressForm as CorePartnerAddressForm
from oscar.apps.partner.models import PartnerAddress
from oscarapps.partner.models import Partner
from django.utils.translation import ugettext_lazy as _
from oscar.core.compat import existing_user_fields, get_user_model
from oscar.core.loading import get_model
from django import forms
from django.utils.translation import pgettext_lazy
from oscarapps.address.models import Locations,States

User = get_user_model()


class PartnerCreateForm(CorePartnerCreateForm):

    class Meta:
        fields = ('name', 'description', 'sex_type', 'image', 'is_active', 'style_preferences',
                  'store_type', 'store_categories', 'street_address', 'post_box', 'city', 'country', 'state', 'zipcode', 'availability')
        labels = {
            'name': _('Store Name'),
        }
        model = Partner


class NewUserForm(CoreNewUserForm):
    class Meta:
        model = User
        fields = existing_user_fields(
            ['username', 'first_name', 'last_name', 'email']) + ['password1', 'password2']


class ExistingUserForm(CoreExistingUserForm):
    class Meta:
        model = User
        fields = existing_user_fields(
            ['username', 'first_name', 'last_name', 'email']) + ['password1', 'password2']


#################
#Brand store type
#################

BrandStoreType = get_model('partner', 'BrandStoreType')


class StoreTypeSearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"BrandStoreType's name", u"Name"))


class StoreTypeCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StoreTypeCreateForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True

    class Meta:
        model = BrandStoreType
        fields = ('name', )



#################
#Brand categories
#################

BrandCategories = get_model('partner', 'BrandCategories')


class BrandCategorySearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"BrandCategories's name", u"Name"))


class BrandCategoryCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BrandCategoryCreateForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True

    class Meta:
        model = BrandCategories
        fields = ('name', 'description', 'type')

#################
#Brand Styles
#################

BrandStyle = get_model('partner', 'BrandStyle')


class BrandStyleSearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"BrandStyle's name", u"Name"))


class BrandStyleCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BrandStyleCreateForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True

    class Meta:
        model = BrandStyle
        fields = ('name', 'description', 'type')
        


class PartnerAddressForm(forms.ModelForm):
    state = forms.ModelChoiceField( required=False, queryset=States.objects.all() )
    class Meta:
        model = Locations
        fields = ('city', 'country', 'state', )


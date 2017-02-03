import re
from oscar.apps.dashboard.partners.forms import PartnerCreateForm as CorePartnerCreateForm
from oscarapps.partner.models import Partner
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.utils.translation import pgettext_lazy
from oscarapps.address.models import Locations, States, Country
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from oscar.core.validators import password_validators
from django.core.validators import validate_email
from oscarapps.partner.models import Category, Style, SubCategory
from oscar.apps.dashboard.partners.forms import PartnerCreateForm as CorePartnerCreateForm
from oscarapps.partner.models import Partner
from oscar.core.compat import get_user_model
from oscar.core.loading import get_model
from oscarapps.address.models import Locations, States



User = get_user_model()


class PartnerCreateForm(forms.Form):

    email = forms.CharField(label='Email', required=True)
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        required=True,
        validators=password_validators)
    password2 = forms.CharField(
        required=True,
        label=_('Confirm Password'),
        widget=forms.PasswordInput)

    name = forms.CharField(label="Store name", required=True)
    image = forms.ImageField(required=False, label="Store image")
    description = forms.CharField(widget=forms.Textarea, label=" Store description")
    city = forms.CharField(label="City", required=True)
    country = forms.ModelChoiceField(label="Country", queryset=Country.objects.all(), required=True)
    state = forms.ModelChoiceField(label="State/County", queryset=States.objects.all(), required=False)
    style = forms.ModelMultipleChoiceField(label="style", queryset=Style.objects.all(), required=True)
    category = forms.ModelMultipleChoiceField(label="Category", queryset=Category.objects.all(), required=True)
    sub_category = forms.ModelMultipleChoiceField(label="Sub category", queryset=SubCategory.objects.all(),
                                                  required=True)
    is_active = forms.BooleanField(initial=True)

    # class Meta:
    #     fields = ('name', 'image', 'description',
    #               'email', 'password1', 'password2', 'first_name', 'last_name',
    #               'city', 'state', 'country',
    #               'style', 'category', 'sub_category', 'is_active'
    #              )
    #     labels = {
    #         'name': _('Store Name'),
    #     }
    #     model = Partner

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')

        if password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."))
        return password2

    def clean(self):
        cleaned_data = super(PartnerCreateForm, self).clean()
        email = cleaned_data.get("email")
        password = self.clean_password2()
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email")

        if User.objects.filter(email=email):
            raise forms.ValidationError("Email already taken")

        password_pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$')
        if password is None or password_pattern.match(password) is None:

            raise forms.ValidationError("Password should have at least 6 characters and one uppercase,"
                                        "lowercase,digit,special character")

        return cleaned_data
      

#################
#Brand Styles
#################

BrandStyle = get_model('partner', 'Style')


class BrandStyleSearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"BrandStyle's name", u"Name"))


class BrandStyleCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BrandStyleCreateForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True

    class Meta:
        model = BrandStyle
        fields = ('name', 'description')






#################
#Brand categories
#################

BrandCategories = get_model('partner', 'Category')


class BrandCategorySearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"BrandCategories's name", u"Name"))


class BrandCategoryCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BrandCategoryCreateForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True

    class Meta:
        model = BrandCategories
        fields = ('name',)







class PartnerAddressForm(forms.ModelForm):
    state = forms.ModelChoiceField(required=False, queryset=States.objects.all())
    class Meta:
        model = Locations
        fields = ('city', 'country', 'state', )


#################
#Brand store type
#################

# BrandStoreType = get_model('partner', 'BrandStoreType')
#
#
# class StoreTypeSearchForm(forms.Form):
#     name = forms.CharField(
#         required=False, label=pgettext_lazy(u"BrandStoreType's name", u"Name"))
#
#
# class StoreTypeCreateForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super(StoreTypeCreateForm, self).__init__(*args, **kwargs)
#
#         self.fields['name'].required = True
#
#     class Meta:
#         model = BrandStoreType
#         fields = ('name', )
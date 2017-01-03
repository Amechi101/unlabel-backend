from oscar.apps.dashboard.partners.forms import PartnerCreateForm as CorePartnerCreateForm
from oscarapps.partner.models import Partner
from django import forms
from django.utils.translation import pgettext_lazy
from oscar.core.loading import get_model
from oscar.apps.dashboard.partners.forms import ExistingUserForm as CoreExistingUserForm


class PartnerCreateForm(CorePartnerCreateForm):
    class Meta:
        fields = ('name', 'brand_website_url', 'brand_description', 'sex_type', 'brand_feature_image', 'brand_isActive', 'brand_style', 'category')
        model = Partner





Influencers = get_model('influencers', 'Influencers')


class InfluencerSearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"Influencers's name", u"Name"))


class InfluencerCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InfluencerCreateForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True

    class Meta:
        model = Influencers
        fields = ('name', 'instagram_url', 'website_url', 'isActive', 'style_Preference', 'industry_choice', 'bio', 'city', 'state_or_country')





Industry = get_model('influencers', 'Industry')


class IndustrySearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"Industry's name", u"Name"))

class IndustryCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(IndustryCreateForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True

    class Meta:
        model = Industry
        fields = ('name', 'description')



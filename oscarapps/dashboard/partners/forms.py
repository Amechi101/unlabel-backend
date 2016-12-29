from oscar.apps.dashboard.partners.forms import PartnerCreateForm as CorePartnerCreateForm
from oscarapps.partner.models import Partner
from oscar.apps.dashboard.partners.forms import PartnerAddressForm




class PartnerCreateForm(CorePartnerCreateForm):
    class Meta:
        fields = ('name', 'website_url', 'description', 'sex_type', 'image', 'is_active', 'style_Preference', 'category')
        model = Partner



from django import forms
from django.utils.translation import pgettext_lazy
from oscar.core.loading import get_classes, get_model

Influencers = get_model('influencers', 'Influencers')

class InfluencerSearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"Influencers's name", u"Name"))


class InfluencerCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InfluencerCreateForm, self).__init__(*args, **kwargs)
        # Partner.name is optional and that is okay. But if creating through
        # the dashboard, it seems sensible to enforce as it's the only field
        # in the form.
        self.fields['name'].required = True

    class Meta:
        model = Influencers
        fields = ('name', 'instagram_url', 'website_url', 'influencer_isActive', 'style_Preference', 'bio')

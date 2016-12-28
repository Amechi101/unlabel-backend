from oscar.apps.dashboard.partners.forms import PartnerCreateForm as CorePartnerCreateForm
from oscarapps.partner.models import Partner,Style
from oscar.apps.dashboard.partners.forms import PartnerAddressForm




class PartnerCreateForm(CorePartnerCreateForm):
    class Meta:
        fields = ('name', 'website_url', 'description', 'sex_type', 'image', 'is_active', 'style_Preference', 'category')
        model = Partner



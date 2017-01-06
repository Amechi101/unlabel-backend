from oscar.apps.dashboard.partners.forms import PartnerCreateForm as CorePartnerCreateForm
from oscarapps.partner.models import Partner
from django.utils.translation import ugettext_lazy as _


class PartnerCreateForm(CorePartnerCreateForm):

    class Meta:
        fields = ('name', 'description', 'sex_type', 'image', 'isActive', 'style_preferences', 'store_type', 'rental_info', 'store_categories')
        labels = {
            'name': _('Store Name'),
        }
        model = Partner


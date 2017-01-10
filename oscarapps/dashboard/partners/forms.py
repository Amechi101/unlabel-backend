from oscar.apps.dashboard.partners.forms import PartnerCreateForm as CorePartnerCreateForm
from oscar.apps.dashboard.partners.forms import NewUserForm as CoreNewUserForm
from oscar.apps.dashboard.partners.forms import ExistingUserForm as CoreExistingUserForm
from oscar.apps.dashboard.partners.forms import PartnerAddressForm as CorePartnerAddressForm
from oscar.apps.partner.models import PartnerAddress
from oscarapps.partner.models import Partner
from django.utils.translation import ugettext_lazy as _
from oscar.core.compat import existing_user_fields, get_user_model
User = get_user_model()


class PartnerCreateForm(CorePartnerCreateForm):

    class Meta:
        fields = ('name', 'description', 'sex_type', 'image', 'isActive', 'style_preferences',
                  'store_type', 'store_categories', 'street_address', 'post_box', 'city',
                  'country', 'state_province', 'availability')
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



class PartnerAddressForm(CorePartnerAddressForm):

     class Meta:
        fields = ('name', 'line1', 'line2', 'line3', 'country',
                  'state', 'line4', 'postcode')
        model = PartnerAddress
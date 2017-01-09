from oscar.apps.dashboard.partners.forms import PartnerCreateForm as CorePartnerCreateForm
from oscar.apps.dashboard.partners.forms import NewUserForm as CoreNewUserForm
from oscar.apps.dashboard.partners.forms import ExistingUserForm as CoreExistingUserForm
from oscar.apps.dashboard.partners.forms import PartnerAddressForm as CorePartnerAddressForm
from oscar.apps.partner.models import PartnerAddress
from oscarapps.partner.models import Partner
from django.utils.translation import ugettext_lazy as _
from oscar.core.compat import existing_user_fields, get_user_model
from django import forms
User = get_user_model()


class PartnerCreateForm(CorePartnerCreateForm):

    class Meta:
        fields = ('name', 'description', 'sex_type', 'image', 'isActive', 'style_preferences', 'store_type', 'rental_info', 'store_categories')
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
        fields = ('name', 'line1', 'line2', 'line3', 'line4', 'country',
                  'state', 'postcode')
        model = PartnerAddress
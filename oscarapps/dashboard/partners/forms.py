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


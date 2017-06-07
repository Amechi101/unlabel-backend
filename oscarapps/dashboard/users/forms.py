from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.apps.dashboard.users.forms import UserSearchForm as CoreUserSearchForm


class UserSearchForm(CoreUserSearchForm):

    Influencer = 'Influencers'
    Brands = 'Brands'
    All = 'All'
    USER_CHOICES = (
        (All, _('All')),
        (Influencer, _('Influencers')),
        (Brands, _('Brands')),
    )

    type = forms.ChoiceField(label="Type", choices=USER_CHOICES,required=False)


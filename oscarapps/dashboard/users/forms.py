from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.apps.dashboard.users.forms import UserSearchForm as CoreUserSearchForm


class UserSearchForm(CoreUserSearchForm):

    Influencers = 'Influencers'
    Brands = 'Brands'
    All = 'All'
    Customers = 'Customers'
    USER_CHOICES = (
        (All, _('All')),
        (Influencers, _('Influencers')),
        (Brands, _('Brands')),
        (Customers, _('Customers')),
    )

    type = forms.ChoiceField(label="Type", choices=USER_CHOICES,required=False)


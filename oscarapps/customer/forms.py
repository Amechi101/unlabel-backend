from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.apps.address.models import Country
from oscar.apps.customer.utils import normalise_email
from oscar.apps.customer.forms import EmailUserCreationForm as BaseEmailUserCreationForm


class EmailUserCreationForm(BaseEmailUserCreationForm):
    first_name = forms.CharField(
        label=_('First name'))
    last_name = forms.CharField(
        label=_('Last name'))
    confirm_email = forms.EmailField(label=_('Confirm email address'))
    dob = forms.DateField(label=_('Date of birth'))
    country = forms.ModelChoiceField(label="Country ",
                                     queryset=Country.objects.all())

    def clean_confirm_email(self):
        email = self.clean_email()
        confirm_email = normalise_email(self.cleaned_data['confirm_email'])
        if email != confirm_email:
            raise forms.ValidationError(
                _("The two email fields didn't match."))
        return confirm_email

    def __init__(self, *args, **kwargs):
        super(EmailUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['dob'].widget.attrs['placeholder'] = 'yyyy-mm-dd'

    def save(self, commit=True):
        user = super(EmailUserCreationForm, self).save(commit=False)
        if commit:
            user.first_name = self.cleaned_data.get('first_name')
            user.last_name = self.cleaned_data.get('last_name')
            user.dob = self.cleaned_data.get('dob')
            user.country = self.cleaned_data.get('country')
            user.save()
        return user
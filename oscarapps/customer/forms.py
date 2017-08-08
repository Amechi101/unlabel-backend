from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from oscar.core.compat import get_user_model, user_is_authenticated
from oscar.apps.address.models import Country
from oscar.apps.customer.utils import normalise_email
from oscar.apps.customer.forms import EmailUserCreationForm as BaseEmailUserCreationForm

User = get_user_model()

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
        if hasattr(self, 'sociallogin'):
            if 'birthday' in self.sociallogin.account.extra_data:
                self.initial['dob'] = self.sociallogin.account.extra_data['birthday']

    def save(self, commit=True):
        user = super(EmailUserCreationForm, self).save(commit=False)
        if commit:
            user.first_name = self.cleaned_data.get('first_name')
            user.last_name = self.cleaned_data.get('last_name')
            user.dob = self.cleaned_data.get('dob')
            user.country = self.cleaned_data.get('country')
            user.save()
        return user

class CustomProfileForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['instance'] = user
        super(CustomProfileForm, self).__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].required = True

    def clean_email(self):
        """
        Make sure that the email address is aways unique as it is
        used instead of the username. This is necessary because the
        unique-ness of email addresses is *not* enforced on the model
        level in ``django.contrib.auth.models.User``.
        """
        email = normalise_email(self.cleaned_data['email'])
        if User._default_manager.filter(
                email__iexact=email).exclude(id=self.user.id).exists():
            raise ValidationError(
                _("A user with this email address already exists"))
        # Save the email unaltered
        return email

    class Meta:
        model = User
        fields = ['first_name','last_name','email','dob','gender', 'country']
from oscarapps.address.models import States
from oscarapps.partner.models import Style, Category, SubCategory
from users.models import User

import re
from django import forms
from django.utils.translation import ugettext_lazy as _
from oscar.apps.address.models import Country


class PartnerSignUpForm(forms.Form):
    """
        Form for Partner signup
    """

    MALE = 'M'
    FEMALE = 'F'
    sex_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    contact_number = forms.CharField(required=True, label="Contact number")
    email = forms.CharField(label='Email', required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=sex_choice, label="Gender", widget=forms.Select(), required=True)
    name = forms.CharField(label="Store Name", required=True)
    image = forms.ImageField(required=False, label="Store Image")
    description = forms.CharField(widget=forms.Textarea, label="Store Description")
    city = forms.CharField(label="City", required=True)
    country = forms.ModelChoiceField(label="Country", queryset=Country.objects.all(), required=True)
    state = forms.ModelChoiceField(label="State", queryset=States.objects.all(), required=False,
                                   help_text="Only select state if your country is USA else leave it unselected")
    style = forms.ModelMultipleChoiceField(label="Style", queryset=Style.objects.all(), required=True, )
    category = forms.ModelMultipleChoiceField(label="Category", queryset=Category.objects.all(), required=True)
    sub_category = forms.ModelMultipleChoiceField(label="Sub category", queryset=SubCategory.objects.all(),
                                                  required=True)


    def clean(self):
        cleaned_data = super(PartnerSignUpForm, self).clean()

        contact_number = cleaned_data.get("contact_number")
        email = cleaned_data.get("email")
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')

        if password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."))

        contact_number_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if contact_number is not None and contact_number_pattern.match(contact_number) is None:
            raise forms.ValidationError("Please enter valid contact number")
        if User.objects.filter(email=email):
            raise forms.ValidationError("Email already in use")
        password_pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
        if password1 is None or password_pattern.match(password1) is None:
            raise forms.ValidationError("Password should have at least 8 characters and one uppercase,"
                                        "lowercase,digit,special character")
        return cleaned_data










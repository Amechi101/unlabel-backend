import re

from django import forms
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from oscar.core.compat import existing_user_fields
from oscar.core.validators import password_validators
from oscar.forms.widgets import ImageInput

from oscarapps.influencers.models import Influencers
from oscarapps.address.models import Country, States
from users.models import User
from oscar.core.loading import get_model

Locations = get_model('address', 'Locations')


class LocationSearchForm(forms.Form):
    city = forms.CharField(
        required=False, label=pgettext_lazy(u"Locations's city", u"City"))


class LocationCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LocationCreateForm, self).__init__(*args, **kwargs)
        self.fields['city'].required = True

    class Meta:
        model = Locations
        fields = ('city', 'country', 'state', 'latitude', 'longitude')


class InfluencerSearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"Influencers's name", u"Name"))


class InfluencerCreateForm(forms.Form):

    MALE = 'M'
    FEMALE = 'F'
    sex_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    email = forms.CharField(label='Email', required=True)
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        required=True,
        help_text="Password should have at least 8 characters with one uppercase,"
                  "lowercase,digit,special character",
        validators=password_validators)
    password2 = forms.CharField(
        required=True,
        help_text="Password should have at least 8 characters with one uppercase,"
                  "lowercase,digit,special character",
        label=_('Confirm Password'),
        widget=forms.PasswordInput)
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    contact_number = forms.CharField(required=True, label="Contact Number")
    image = forms.ImageField(label="Profile Image", required=False)
    bio = forms.CharField(widget=forms.Textarea, label="Bio", help_text="Few words about yourself")
    # city = forms.CharField(label="City", required=True)
    # country = forms.ModelChoiceField(label="Country", queryset=Country.objects.all(), required=True)
    # state = forms.ModelChoiceField(label="State", queryset=States.objects.all(), required=False,
    #                                help_text="Only select state if your country is USA else leave it unselected")
    location = forms.ModelChoiceField(label="Location", queryset=Locations.objects.all(), required=True)
    gender = forms.ChoiceField(choices=sex_choice, label="Gender", widget=forms.Select(), required=True)
    height = forms.IntegerField(required=True, min_value=0, label="Height", help_text="Enter size in inches")
    chest_or_bust = forms.IntegerField(required=True, min_value=0, label="Chest / Bust", help_text="Enter size in inches")
    hips = forms.IntegerField(required=True, min_value=0, label="Hip", help_text="Enter size in inches")
    waist = forms.IntegerField(required=True, min_value=0, label="Waist", help_text="Enter size in inches")
    is_active = forms.BooleanField(initial=True)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        password_pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')

        if password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."))
        if password_pattern.match(password2) is None:
                raise forms.ValidationError("Password should have at least 8 characters and one uppercase,"
                                        "lowercase,digit,special character")
        return password2

    def clean(self):
        cleaned_data = super(InfluencerCreateForm, self).clean()
        height = cleaned_data.get("height")
        chest_or_bust = cleaned_data.get("chest_or_bust")
        hips = cleaned_data.get("hips")
        waist = cleaned_data.get("waist")
        contact_number = cleaned_data.get("contact_number")
        email = cleaned_data.get("email")
        if height is not None and len(str(height)) > 2:
            raise forms.ValidationError("Please enter valid height in Inches")
        if chest_or_bust is not None and len(str(chest_or_bust)) > 2:
            raise forms.ValidationError("Please enter valid Chest/Bust size in Inches")
        if hips is not None and len(str(hips)) > 2:
            raise forms.ValidationError("Please enter valid hip size in Inches")
        if waist is not None and len(str(waist)) > 2:
            raise forms.ValidationError("Please enter valid waist size in Inches")
        contact_number_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if contact_number is None or contact_number_pattern.match(contact_number) is None:
            raise forms.ValidationError("Please enter valid contact number")
        if User.objects.filter(email__iexact=email):
            raise forms.ValidationError("Email already taken")

        return cleaned_data


class InfluencerManageForm(forms.ModelForm):
    MALE = 'M'
    FEMALE = 'F'
    sex_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    auto_id = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
    # city = forms.CharField(label="City", required=True)
    # country = forms.ModelChoiceField(label="Country", queryset=Country.objects.all(), required=True)
    # state = forms.ModelChoiceField(label="State/County", queryset=States.objects.all(), required=False,
    #                                help_text="Only select state if your country is USA else leave it unselected")
    location = forms.ModelChoiceField(label="Location", queryset=Locations.objects.all(), required=True)
    is_active = forms.BooleanField(required=False)
    image = forms.ImageField(widget=ImageInput)
    gender = forms.ChoiceField()

    def __init__(self,  *args, **kwargs):
        super(InfluencerManageForm, self).__init__(*args, **kwargs)
        print(self.instance.users.gender)
        self.fields['gender'].choices = self.sex_choice
        self.fields['gender'].initial = self.instance.users.gender

    # password1 = forms.CharField(
    #     label=_('Password'),
    #     widget=forms.PasswordInput,
    #     required=True,
    #     validators=password_validators)
    # password2 = forms.CharField(
    #     required=True,
    #     label=_('Confirm Password'),
    #     widget=forms.PasswordInput)



    class Meta:
        model = Influencers
        fields = ('auto_id', 'is_active',
                  'bio', 'image',
                  'gender',
                  'height', 'chest_or_bust', 'hips', 'waist',
                  # 'city', 'country', 'state',
                  'location'
                  )



    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1', '')
    #     password2 = self.cleaned_data.get('password2', '')
    #     password_pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$')
    #
    #     if password1 != password2:
    #         raise forms.ValidationError(
    #             _("The two password fields didn't match."))
    #     if password_pattern.match(password2) is None:
    #             raise forms.ValidationError("Password should have at least 6 characters and one uppercase,"
    #                                     "lowercase,digit,special character")
    #     return password2

    def save(self, commit=True):
        instance = super(InfluencerManageForm, self).save(commit=False)
        # instance.location.city = self.cleaned_data['city']
        # try:
        #     state = States.objects.get(name=self.cleaned_data['state'])
        # except ObjectDoesNotExist:
        #     state = None
        # instance.location.state = state
        # instance.location.country = Country.objects.get(printable_name=self.cleaned_data['country'])
        instance.users.is_active = self.cleaned_data['is_active']
        instance.users.gender = self.cleaned_data['gender']
        instance.location = self.cleaned_data['location']
        if commit:
            # instance.location.save()
            instance.users.save()
            instance.save()
        return instance


class ExistingUserForm(forms.ModelForm):
    """
    Slightly different form that makes
    * makes saving password optional
    * doesn't regenerate username
    * doesn't allow changing email till #668 is resolved
    """
    # role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect,
    #                          label=_('User role'))

    first_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
    gender = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
    # password1 = forms.CharField(
    #     label=_('Password'),
    #     widget=forms.PasswordInput,
    #     required=False,
    #     validators=password_validators)
    # password2 = forms.CharField(
    #     required=False,
    #     label=_('Confirm Password'),
    #     widget=forms.PasswordInput)
    #
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1', '')
    #     password2 = self.cleaned_data.get('password2', '')
    #
    #     if password1 != password2:
    #         raise forms.ValidationError(
    #             _("The two password fields didn't match."))
    #     return password2

    # def __init__(self, *args, **kwargs):
    #     user = kwargs['instance']
    #     role = 'staff' if user.is_staff else 'limited'
    #     kwargs.get('initial', {}).setdefault('role', role)
    #     super(ExistingUserForm, self).__init__(*args, **kwargs)

    def save(self):
        # role = self.cleaned_data.get('role', 'none')
        user = super(ExistingUserForm, self).save(commit=False)
        # user.is_staff = role == 'staff'
        user.save()

        # dashboard_perm = Permission.objects.get(
        #     codename='dashboard_access', content_type__app_label='partner')
        # user_has_perm = user.user_permissions.filter(
        #     pk=dashboard_perm.pk).exists()
        # if role == 'limited' and not user_has_perm:
        #     user.user_permissions.add(dashboard_perm)
        # elif role == 'staff' and user_has_perm:
        #     user.user_permissions.remove(dashboard_perm)
        return user

    class Meta:
        model = User
        fields = existing_user_fields(
            ['username', 'first_name', 'last_name','email']) + ['contact_number', 'gender']
        exclude = ('password1',)

import re

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.utils.translation import pgettext_lazy
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from oscar.core.loading import get_model
from oscar.core.validators import password_validators
from oscar.apps.catalogue.models import ProductClass
from oscar.core.compat import existing_user_fields
from django.contrib.auth.models import Permission

from oscarapps.address.models import Locations, States, Country
from oscarapps.partner.models import Partner, Category, Style, SubCategory, RentalInformation
from users.models import User


class PartnerCreateForm(forms.Form):

    email = forms.CharField(label='Email', required=True)
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
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
    name = forms.CharField(label="Store Name", required=True)
    image = forms.ImageField(required=False, label="Store Image")
    description = forms.CharField(widget=forms.Textarea, label=" Store Description")
    city = forms.CharField(label="City", required=True)
    country = forms.ModelChoiceField(label="Country", queryset=Country.objects.all(), required=True)
    state = forms.ModelChoiceField(label="State", queryset=States.objects.all(), required=False,
                                   help_text="Only select state if your country is USA else leave it unselected")
    style = forms.ModelMultipleChoiceField(label="Style", queryset=Style.objects.all(), required=True,)
    category = forms.ModelMultipleChoiceField(label="Store Type", queryset=Category.objects.all(), required=True)
    sub_category = forms.ModelMultipleChoiceField(label="Specialization", queryset=SubCategory.objects.all(),
                                                  required=True)
    is_active = forms.BooleanField(initial=True, help_text="Uncheck to deactivate store")

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
        cleaned_data = super(PartnerCreateForm, self).clean()
        email = cleaned_data.get("email")
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email")
        if User.objects.filter(email__iexact=email):
            raise forms.ValidationError("Email already taken")
        return cleaned_data


class PartnerManageForm(forms.ModelForm):

    city = forms.CharField(label="City", required=True)
    country = forms.ModelChoiceField(label="Country", queryset=Country.objects.all(), required=True)
    state = forms.ModelChoiceField(label="State", queryset=States.objects.all(), required=False,
                                   help_text="Only select state if your country is USA else leave it unselected")
    is_active = forms.BooleanField(required=False, help_text="Check|Un check to activate|deactivate store")

    # password1 = forms.CharField(
    #     label=_('Change Password'),
    #     widget=forms.PasswordInput,
    #     required=False,
    #     validators=password_validators)
    #
    # password2 = forms.CharField(
    #     required=False,
    #     label=_('Confirm Password'),
    #     widget=forms.PasswordInput)

    class Meta:
        model = Partner
        fields = (
            'name', 'image', 'description',
            'city', 'country', 'state',
            'style', 'category', 'sub_category', 'is_active',
            # 'password1', 'password2',
            )

        labels = {
            'name': 'Store Name',
            'style': 'Selected Styles',
            'category': 'Selected Store Types',
            'sub_category': 'Selected Specializations'
        }


    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1', '')
    #     password2 = self.cleaned_data.get('password2', '')
    #     password_pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$')
    #     if password1!="" and password1 is not None:
    #         if password1 != password2:
    #             raise forms.ValidationError(
    #                 _("The two password fields didn't match."))
    #         if password_pattern.match(password2) is None:
    #                 raise forms.ValidationError("Password should have at least 6 characters and one uppercase,"
    #                                         "lowercase,digit,special character")
    #         return password2


    def save(self, commit=True):
        instance = super(PartnerManageForm, self).save(commit=False)
        instance.location.city = self.cleaned_data['city']
        instance.location.country = Country.objects.get(printable_name=self.cleaned_data['country'])
        instance.is_active = self.cleaned_data['is_active']
        instance.style = self.cleaned_data['style']
        instance.category = self.cleaned_data['category']
        instance.sub_category = self.cleaned_data['sub_category']

        if str(self.cleaned_data['country']) == "United States":
            try:
                state = States.objects.get(name=self.cleaned_data['state'])
            except:
                state = None
        else:
            state = None
        instance.location.state = state
        instance.location.country = Country.objects.get(printable_name=self.cleaned_data['country'])
        if commit:
            instance.location.save()
            instance.save()
        return instance


class PartnerRentalInfoForm(forms.ModelForm):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'
    day_choice = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )
    AM = 'AM'
    PM = 'PM'
    time_period_choice = (
        (AM, 'AM'),
        (PM, 'PM'),
    )
    day = forms.MultipleChoiceField(label="Days", choices=day_choice, help_text='Choose rental days')
    start_time = forms.TimeField(label="Start Time", help_text="Enter time in 12 hours format. Ex 11:30")
    start_time_period = forms.ChoiceField(label='Start Time Period', choices=time_period_choice)
    end_time = forms.TimeField(label="End Time", help_text="Enter time in 12 hours format.  Ex 11:30")
    end_time_period = forms.ChoiceField(label='End Time Period', choices=time_period_choice)
    contact_number = forms.CharField(required=True, label="Contact Number")

    class Meta:
        model = RentalInformation
        fields = ('day', 'start_time', 'start_time_period', 'end_time', 'end_time_period',
                  'contact_number',
                  'post_box', 'zipcode', 'city', 'country', 'state',)

        labels = {'zipcode': 'Zip Code'}

#################
#Brand Styles
#################

BrandStyle = get_model('partner', 'Style')


class BrandStyleSearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"BrandStyle's name", u"Name"))


class BrandStyleCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BrandStyleCreateForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True

    class Meta:
        model = BrandStyle
        fields = ('name', 'description')






#################
#Brand categories
#################

BrandCategories = get_model('partner', 'Category')


class BrandCategorySearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"BrandCategories's name", u"Name"))


class BrandCategoryCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BrandCategoryCreateForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True

    class Meta:
        model = BrandCategories
        fields = ('name', 'description')





#################
#Brand store type
#################

BrandSubCategory = get_model('partner', 'SubCategory')


class SubCategorySearchForm(forms.Form):
    name = forms.CharField(
        required=False, label=pgettext_lazy(u"BrandSubCategory's name", u"Name"))


class SubCategoryCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubCategoryCreateForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True

    class Meta:
        model = BrandSubCategory
        fields = ('name','description' )

ROLE_CHOICES = (
    ('staff', _('Full dashboard access')),
    ('limited', _('Limited dashboard access')),
)



class ExistingUserForm(forms.ModelForm):
    """
    Slightly different form that makes
    * makes saving password optional
    * doesn't regenerate username
    * doesn't allow changing email till #668 is resolved
    """
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect,
                             label=_('User role'))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))

    def __init__(self, *args, **kwargs):
        user = kwargs['instance']
        role = 'staff' if user.is_staff else 'limited'
        kwargs.get('initial', {}).setdefault('role', role)
        super(ExistingUserForm, self).__init__(*args, **kwargs)

    def save(self):
        role = self.cleaned_data.get('role', 'none')
        user = super(ExistingUserForm, self).save(commit=False)
        user.is_staff = role == 'staff'
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        user.save()

        dashboard_perm = Permission.objects.get(
            codename='dashboard_access', content_type__app_label='partner')
        user_has_perm = user.user_permissions.filter(
            pk=dashboard_perm.pk).exists()
        if role == 'limited' and not user_has_perm:
            user.user_permissions.add(dashboard_perm)
        elif role == 'staff' and user_has_perm:
            user.user_permissions.remove(dashboard_perm)
        return user


    class Meta:
        model = User
        fields = existing_user_fields(
            ['first_name', 'last_name', 'email'])

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
from oscarapps.partner.models import Partner, Category, Style, SubCategory, RentalInformation, RentalTime
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

    # city = forms.CharField(label="City", required=True)
    # country = forms.ModelChoiceField(label="Country", queryset=Country.objects.all(), required=True)
    # state = forms.ModelChoiceField(label="State", queryset=States.objects.all(), required=False,
    #                                help_text="Only select state if your country is USA else leave it unselected")
    # location = forms.ModelChoiceField(label="Location", queryset=Locations.objects.all(), required=True)

    style = forms.ModelMultipleChoiceField(label="Style", queryset=Style.objects.all(), required=True,)
    category = forms.ModelMultipleChoiceField(label="Store Type", queryset=Category.objects.all(), required=True)
    sub_category = forms.ModelMultipleChoiceField(label="Specialization", queryset=SubCategory.objects.all(),
                                                  required=True)
    loc = forms.CharField(label="Location", required=True)
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

    # city = forms.CharField(label="City", required=True)
    # country = forms.ModelChoiceField(label="Country", queryset=Country.objects.all(), required=True)
    # state = forms.ModelChoiceField(label="State", queryset=States.objects.all(), required=False,
    #                                help_text="Only select state if your country is USA else leave it unselected")
    is_active = forms.BooleanField(required=False, help_text="Check|Un check to activate|deactivate store")
    # location = forms.ModelChoiceField(label="Location", queryset=Locations.objects.all(), required=True)
    loc = forms.CharField(label="Location", required=True)

    class Meta:
        model = Partner
        fields = (
            'name', 'image', 'description',
            # 'city', 'country', 'state',
            'style', 'category', 'sub_category', 'loc', 'is_active',
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
        loc = str(self.cleaned_data['loc']).split(', ')
        try:
            instance.location.city = ", ".join(str(x) for x in loc[:-2])
            instance.location.state = str(loc[-2:-1][0])
            if str(loc[-1:][0]) == "United States":
                instance.location.country = "USA"
            else:
                instance.location.country = str(loc[-1:][0])
            instance.location.is_brand_location = True
        except:
            city = ", ".join(str(x) for x in loc[:-2])
            state = str(loc[-2:-1][0])
            if str(loc[-1:][0]) == "United States":
                country = "USA"
            else:
                country = str(loc[-1:][0])
            partner_location = Locations.objects.create(city=city,
                                            state=state,
                                            country=country,
                                            is_brand_location=True,
                                            )
            instance.location = partner_location
        instance.is_active = self.cleaned_data['is_active']
        instance.style = self.cleaned_data['style']
        instance.category = self.cleaned_data['category']
        instance.sub_category = self.cleaned_data['sub_category']
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
    day = forms.MultipleChoiceField(label="Day 1", choices=day_choice, help_text='Choose rental days')
    start_time = forms.TimeField(label="Start Time", help_text="Enter time in 12 hours format. Ex 11:30")
    start_time_period = forms.ChoiceField(label='Start Time Period', choices=time_period_choice)
    end_time = forms.TimeField(label="End Time", help_text="Enter time in 12 hours format.  Ex 11:30")
    end_time_period = forms.ChoiceField(label='End Time Period', choices=time_period_choice)

    day_1 = forms.MultipleChoiceField(label="Day 2", choices=day_choice, help_text='Choose rental days', required=False)
    start_time_1 = forms.TimeField(label="Start Time", help_text="Enter time in 12 hours format. Ex 11:30", required=False)
    start_time_period_1 = forms.ChoiceField(label='Start Time Period', choices=time_period_choice, required=False)
    end_time_1 = forms.TimeField(label="End Time", help_text="Enter time in 12 hours format.  Ex 11:30", required=False)
    end_time_period_1 = forms.ChoiceField(label='End Time Period', choices=time_period_choice, required=False)

    day_2 = forms.MultipleChoiceField(label="Day 3", choices=day_choice, help_text='Choose rental days', required=False)
    start_time_2 = forms.TimeField(label="Start Time", help_text="Enter time in 12 hours format. Ex 11:30", required=False)
    start_time_period_2 = forms.ChoiceField(label='Start Time Period', choices=time_period_choice, required=False)
    end_time_2 = forms.TimeField(label="End Time", help_text="Enter time in 12 hours format.  Ex 11:30", required=False)
    end_time_period_2 = forms.ChoiceField(label='End Time Period', choices=time_period_choice, required=False)

    day_3 = forms.MultipleChoiceField(label="Day 4", choices=day_choice, help_text='Choose rental days', required=False)
    start_time_3 = forms.TimeField(label="Start Time", help_text="Enter time in 12 hours format. Ex 11:30", required=False)
    start_time_period_3 = forms.ChoiceField(label='Start Time Period', choices=time_period_choice, required=False)
    end_time_3 = forms.TimeField(label="End Time", help_text="Enter time in 12 hours format.  Ex 11:30", required=False)
    end_time_period_3 = forms.ChoiceField(label='End Time Period', choices=time_period_choice, required=False)

    day_4 = forms.MultipleChoiceField(label="Day 5", choices=day_choice, help_text='Choose rental days', required=False)
    start_time_4 = forms.TimeField(label="Start Time", help_text="Enter time in 12 hours format. Ex 11:30", required=False)
    start_time_period_4 = forms.ChoiceField(label='Start Time Period', choices=time_period_choice, required=False)
    end_time_4 = forms.TimeField(label="End Time", help_text="Enter time in 12 hours format.  Ex 11:30", required=False)
    end_time_period_4 = forms.ChoiceField(label='End Time Period', choices=time_period_choice, required=False)

    day_5 = forms.MultipleChoiceField(label="Day 6", choices=day_choice, help_text='Choose rental days', required=False)
    start_time_5 = forms.TimeField(label="Start Time", help_text="Enter time in 12 hours format. Ex 11:30", required=False)
    start_time_period_5 = forms.ChoiceField(label='Start Time Period', choices=time_period_choice, required=False)
    end_time_5 = forms.TimeField(label="End Time", help_text="Enter time in 12 hours format.  Ex 11:30", required=False)
    end_time_period_5 = forms.ChoiceField(label='End Time Period', choices=time_period_choice, required=False)

    day_6 = forms.MultipleChoiceField(label="Day 7", choices=day_choice, help_text='Choose rental days', required=False)
    start_time_6 = forms.TimeField(label="Start Time", help_text="Enter time in 12 hours format. Ex 11:30", required=False)
    start_time_period_6 = forms.ChoiceField(label='Start Time Period', choices=time_period_choice, required=False)
    end_time_6 = forms.TimeField(label="End Time", help_text="Enter time in 12 hours format.  Ex 11:30", required=False)
    end_time_period_6 = forms.ChoiceField(label='End Time Period', choices=time_period_choice, required=False)

    contact_number = forms.CharField(required=True, label="Contact Number")
    loc = forms.CharField(label="Location", required=True)

    class Meta:
        model = RentalInformation
        fields = ('day', 'start_time', 'start_time_period', 'end_time', 'end_time_period',
                  'contact_number',
                  'post_box', 'zipcode', 'loc')

        labels = {'zipcode': 'Zip Code'}

    def save(self, commit=True):
        instance = super(PartnerRentalInfoForm, self).save(commit=False)
        loc = str(self.cleaned_data['loc']).split(', ')
        rental_day = []
        instance.city = ", ".join(str(x) for x in loc[:-2])
        instance.state = str(loc[-2:-1][0])
        if str(loc[-1:][0]) == "United States":
            instance.country = "USA"
        else:
            instance.country = str(loc[-1:][0])

        if self.cleaned_data['day']:
            obj = self.rental_days_time(self.cleaned_data['day'][0], self.cleaned_data['start_time'],
                                        self.cleaned_data['start_time_period'], self.cleaned_data['end_time'],
                                        self.cleaned_data['end_time_period'])
            rental_day.append(obj)

        if self.cleaned_data['day_1']:
            obj = self.rental_days_time(self.cleaned_data['day_1'][0], self.cleaned_data['start_time_1'],
                                        self.cleaned_data['start_time_period_1'], self.cleaned_data['end_time_1'],
                                        self.cleaned_data['end_time_period_1'])
            rental_day.append(obj)

        if self.cleaned_data['day_2']:
            obj = self.rental_days_time(self.cleaned_data['day_2'][0], self.cleaned_data['start_time_2'],
                                        self.cleaned_data['start_time_period_2'], self.cleaned_data['end_time_2'],
                                        self.cleaned_data['end_time_period_2'])
            rental_day.append(obj)

        if self.cleaned_data['day_3']:
            obj = self.rental_days_time(self.cleaned_data['day_3'][0], self.cleaned_data['start_time_3'],
                                        self.cleaned_data['start_time_period_3'], self.cleaned_data['end_time_3'],
                                        self.cleaned_data['end_time_period_3'])
            rental_day.append(obj)

        if self.cleaned_data['day_4']:
            obj = self.rental_days_time(self.cleaned_data['day_4'][0], self.cleaned_data['start_time_4'],
                                        self.cleaned_data['start_time_period_4'], self.cleaned_data['end_time_4'],
                                        self.cleaned_data['end_time_period_4'])
            rental_day.append(obj)

        if self.cleaned_data['day_5']:
            obj = self.rental_days_time(self.cleaned_data['day_5'][0], self.cleaned_data['start_time_5'],
                                        self.cleaned_data['start_time_period_5'], self.cleaned_data['end_time_5'],
                                        self.cleaned_data['end_time_period_5'])
            rental_day.append(obj)

        if self.cleaned_data['day_6']:
            obj = self.rental_days_time(self.cleaned_data['day_6'][0], self.cleaned_data['start_time_6'],
                                        self.cleaned_data['start_time_period_6'], self.cleaned_data['end_time_6'],
                                        self.cleaned_data['end_time_period_6'])
            rental_day.append(obj)

        if commit:
            instance.rental_time = rental_day
            instance.save()
        return instance

    def rental_days_time(self, day, start_time, start_time_period, end_time, end_time_period):
        obj = RentalTime.objects.create()
        obj.day = day
        obj.start_time = start_time
        obj.start_time_period = start_time_period
        obj.end_time = end_time
        obj.end_time_period = end_time_period
        obj.save()
        return obj
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
        fields = ('name','description')






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
        fields = ('name',)





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
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        required=False,
        validators=password_validators)
    password2 = forms.CharField(
        required=False,
        label=_('Confirm Password'),
        widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')

        if password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."))
        return password2

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        print(self.request.user)
        super(ExistingUserForm, self).__init__(*args, **kwargs)
        user = kwargs['instance']
        if self.request.user.is_brand:
            self.fields["first_name"].widget = forms.TextInput()
            self.fields["last_name"].widget = forms.TextInput()
            del self.fields['role']
        else:
            del self.fields['password1']
            del self.fields['password2']
        role = 'staff' if user.is_staff else 'limited'
        kwargs.get('initial', {}).setdefault('role', role)


    def save(self):
        role = self.cleaned_data.get('role', 'none')
        user = super(ExistingUserForm, self).save(commit=False)
        user.is_staff = role == 'staff'
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
            ['email', 'first_name', 'last_name']) + ['password1', 'password2']
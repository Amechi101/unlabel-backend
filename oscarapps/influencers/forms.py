#
# from django import forms
# from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import Permission
#
# from oscar.apps.customer.forms import EmailUserCreationForm
# from oscar.core.compat import existing_user_fields, get_user_model
# from oscar.core.loading import get_model
# from oscar.core.validators import password_validators
# from oscar.apps.dashboard.partners.forms import ExistingUserForm as CoreExistingUserForm
# from oscar.apps.dashboard.partners.forms import NewUserForm as CoreNewUserForm
#
# User = get_user_model()
# Influencer = get_model('influencer', 'Influencer')
# # class ExistingUserForm(CoreExistingUserForm):
# #     def save(self):
# #         role = self.cleaned_data.get('role', 'none')
# #         user = super(ExistingUserForm, self).save(commit=False)
# #         user.is_staff = role == 'staff'
# #         if self.cleaned_data['password1']:
# #             user.set_password(self.cleaned_data['password1'])
# #         user.save()
# #
# #         dashboard_perm = Permission.objects.get(
# #             codename='dashboard_access', content_type__app_label='influencer')
# #         user_has_perm = user.user_permissions.filter(
# #             pk=dashboard_perm.pk).exists()
# #         if role == 'limited' and not user_has_perm:
# #             user.user_permissions.add(dashboard_perm)
# #         elif role == 'staff' and user_has_perm:
# #             user.user_permissions.remove(dashboard_perm)
# #         return user
# #
# #
# # class NewUserForm(CoreNewUserForm):
# #
# #     def __init__(self, influencer, *args, **kwargs):
# #         self.influencer = influencer
# #         print(influencer,"=======")
# #         super(NewUserForm, self).__init__(*args, **kwargs)
# #
# #     def save(self):
# #         role = self.cleaned_data.get('role', 'limited')
# #         user = super(NewUserForm, self).save(commit=False)
# #         user.is_staff = role == 'staff'
# #         user.save()
# #         self.influencer.users.add(user)
# #         if role == 'limited':
# #             dashboard_access_perm = Permission.objects.get(
# #                 codename='dashboard_access', content_type__app_label='influencer')
# #             user.user_permissions.add(dashboard_access_perm)
# #         return user
#
# ROLE_CHOICES = (
#     ('staff', _('Full dashboard access')),
#     ('limited', _('Limited dashboard access')),
# )
#
#
# class NewUserForm(EmailUserCreationForm):
#     role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect,
#                              label=_('User role'), initial='limited')
#
#     def __init__(self, influencer, *args, **kwargs):
#         self.influencer = influencer
#         super(NewUserForm, self).__init__(host=None, *args, **kwargs)
#
#     def save(self):
#         role = self.cleaned_data.get('role', 'limited')
#         user = super(NewUserForm, self).save(commit=False)
#         user.is_staff = role == 'staff'
#         user.save()
#         self.partner.users.add(user)
#         if role == 'limited':
#             dashboard_access_perm = Permission.objects.get(
#                 codename='dashboard_access', content_type__app_label='influencers')
#             user.user_permissions.add(dashboard_access_perm)
#         return user
#
#     class Meta:
#         model = User
#         fields = existing_user_fields(
#             ['first_name', 'last_name', 'email']) + ['password1', 'password2']
#
#
# class ExistingUserForm(forms.ModelForm):
#     """
#     Slightly different form that makes
#     * makes saving password optional
#     * doesn't regenerate username
#     * doesn't allow changing email till #668 is resolved
#     """
#     role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect,
#                              label=_('User role'))
#     password1 = forms.CharField(
#         label=_('Password'),
#         widget=forms.PasswordInput,
#         required=False,
#         validators=password_validators)
#     password2 = forms.CharField(
#         required=False,
#         label=_('Confirm Password'),
#         widget=forms.PasswordInput)
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1', '')
#         password2 = self.cleaned_data.get('password2', '')
#
#         if password1 != password2:
#             raise forms.ValidationError(
#                 _("The two password fields didn't match."))
#         return password2
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs['instance']
#         role = 'staff' if user.is_staff else 'limited'
#         kwargs.get('initial', {}).setdefault('role', role)
#         super(ExistingUserForm, self).__init__(*args, **kwargs)
#
#     def save(self):
#         role = self.cleaned_data.get('role', 'none')
#         user = super(ExistingUserForm, self).save(commit=False)
#         user.is_staff = role == 'staff'
#         if self.cleaned_data['password1']:
#             user.set_password(self.cleaned_data['password1'])
#         user.save()
#
#         dashboard_perm = Permission.objects.get(
#             codename='dashboard_access', content_type__app_label='influencers')
#         user_has_perm = user.user_permissions.filter(
#             pk=dashboard_perm.pk).exists()
#         if role == 'limited' and not user_has_perm:
#             user.user_permissions.add(dashboard_perm)
#         elif role == 'staff' and user_has_perm:
#             user.user_permissions.remove(dashboard_perm)
#         return user
#
#     class Meta:
#         model = User
#         fields = existing_user_fields(
#             ['first_name', 'last_name']) + ['password1', 'password2']
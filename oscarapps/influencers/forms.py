from oscar.apps.dashboard.partners.forms import ExistingUserForm as CoreExistingUserForm
from oscar.apps.dashboard.partners.forms import NewUserForm as CoreNewUserForm
from django.contrib.auth.models import Permission



class ExistingUserForm(CoreExistingUserForm):
    def save(self):
        role = self.cleaned_data.get('role', 'none')
        user = super(ExistingUserForm, self).save(commit=False)
        user.is_staff = role == 'staff'
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        user.save()

        dashboard_perm = Permission.objects.get(
            codename='dashboard_access', content_type__app_label='influencer')
        user_has_perm = user.user_permissions.filter(
            pk=dashboard_perm.pk).exists()
        if role == 'limited' and not user_has_perm:
            user.user_permissions.add(dashboard_perm)
        elif role == 'staff' and user_has_perm:
            user.user_permissions.remove(dashboard_perm)
        return user

class NewUserForm(CoreNewUserForm):

    def __init__(self, influencer, *args, **kwargs):
        self.influencer = influencer
        super(NewUserForm, self).__init__(host=None, *args, **kwargs)

    def save(self):
        role = self.cleaned_data.get('role', 'limited')
        user = super(NewUserForm, self).save(commit=False)
        user.is_staff = role == 'staff'
        user.save()
        self.influencer.users.add(user)
        if role == 'limited':
            dashboard_access_perm = Permission.objects.get(
                codename='dashboard_access', content_type__app_label='influencer')
            user.user_permissions.add(dashboard_access_perm)
        return user
from django import forms
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.forms import (
   UserCreationForm,
)

from .models import User


class UserCreationForm(forms.ModelForm):
   class Meta:
       model = User
       fields = ('email',)

   def save(self, commit=True):
       # Save the provided password in hashed format
       user = super(UserCreationForm, self).save(commit=False)
       user.set_password(self.cleaned_data["password"])
       if commit:
           user.save()
       return user


class CustomUserAdmin(UserAdmin):
   # The forms to add and change user instances
   add_form = UserCreationForm
   list_display = ("email",)
   ordering = ("email",)

   fieldsets = (
       (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'contact_number', 'is_influencer', 'is_brand', 'gender','is_active')}),
   )
   add_fieldsets = (
       (None, {
           'classes': ('wide',),
           'fields': (
               'email', 'password', 'first_name', 'last_name', 'is_influencer', 'is_superuser', 'is_staff',
               'is_active')}
       ),
   )

   filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(Permission)
admin.site.register(ContentType)
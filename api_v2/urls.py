from django.conf.urls import include, url,patterns
from rest_framework import routers
from .customer import views as customerViews

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [

	# api's
	# url(r'^labels-api/', include() ) ,
    url(r'customer_register/',
        customerViews.CustomerRegisterView.as_view(),name='register_view'),

    url(r'customer_update_password/',
        customerViews.CustomerPasswordUpdateView.as_view(), name='password_update_view'),

    url(r'customer_forgot_password/',
        customerViews.CustomerForgotPassword.as_view(),name='customer_forgot_password_view'),


]

urlpatterns = patterns('django.contrib.auth.views',
   # url(r'^login/$', 'login', {
   #     'template_name': 'profiles/login.html','authentication_form':LoginForm}, name='user-login'),
   # url(r'^password/reset/$', 'password_reset', name='password_reset',
   #     kwargs={'post_reset_redirect' : '/accounts/password-reset-done',
   #     'template_name': 'profiles/password_reset.html','password_reset_form':PasswordForm}),
   url(r'^password-reset-done/$', 'password_reset_done',
       {'template_name': 'profiles/password_reset_done.html',},name='password-reset-done'),
   url(r'^password/reset/confirm/(?P<uidb36>[0-9a-zA-Z]{1,13})-(?P<token>.+)/$',
       'password_reset_confirm',
       {'template_name': 'profiles/password_reset_confirm.html',},
       name='password-reset-confirm'),
   url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
   'password_reset_confirm',{'template_name': 'accounts/password_reset_confirm.html',},
   name='password_reset_confirm'),
   url(r'^password-reset-complete', 'password_reset_complete', {
       'template_name': 'accounts/password_reset_complete.html',
   }, name='password_reset_complete'),
   )
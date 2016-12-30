from django.conf.urls import include, url,patterns
from rest_framework import routers
from .customer import views as customerViews
from .address import views as addressViews

#####   customer urls   #####
urlpatterns = [
	# api's
	# url(r'^labels-api/', include() ) ,
    url(r'customer_register/',
        customerViews.CustomerRegisterView.as_view(),name='register_view'),

    url(r'customer_update_password/',
        customerViews.CustomerPasswordUpdateView.as_view(), name='password_update_view'),

    url(r'customer_forgot_password/',
        customerViews.CustomerForgotPassword.as_view(),name='customer_forgot_password_view'),

    url(r'customer_profile_update',
        customerViews.CustomerProfileUpdateView.as_view(),name='customer_profile_update_view')

]

##### address urls  #####

urlpatterns = urlpatterns + [

    # url(r'add_address/',)
]


urlpatterns = urlpatterns + patterns(
                'django.contrib.auth.views',
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
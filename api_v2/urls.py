from django.conf.urls import include, url
from rest_framework import routers
from .customer import views as customerViews

urlpatterns = [

	# api's
	# url(r'^labels-api/', include() ) ,
    url(r'customer_register/',customerViews.CustomerRegisterView.as_view(),name='register_view'),
    url(r'customer_update_password/',customerViews.CustomerPasswordUpdateView.as_view(), name='password_update_view')

]
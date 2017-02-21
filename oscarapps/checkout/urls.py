from django.conf.urls import url

from oscarapps.checkout import views

urlpatterns = [

    url(r'^charge/$',  views.charge, name='charge'),
    url(r'^transfer/$',  views.transfer, name='transfer'),
]

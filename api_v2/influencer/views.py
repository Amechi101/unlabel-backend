from django.views.generic import View
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import tokens

from rest_framework import permissions, authentication


class InfluencerSignUpView(View):

    def get(self,request,uidb64,*args,**kwargs):
        print("----------------> ",(urlsafe_base64_decode(uidb64)).decode("utf-8"))

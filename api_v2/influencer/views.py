from __future__ import unicode_literals
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail.message import EmailMessage
from users.models import User
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes


class InfluencerForgotPassword(APIView):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('post',)

    def post(self, request, *args, **kwargs):
        # if request.data["email"]:
        try:
            if User.objects.filter(email__iexact=request.data["email"]).exists():
                current_site = Site.objects.get_current()
                domain = current_site.domain
                user = User.objects.get(email__iexact=request.data["email"])
                context = {
                    'domain': domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                try:
                    tosend = context['protocol'] + '://' + context['domain'] + '/api_v2/reset/' + context['uid'].decode(
                        "utf-8") + '/' + context['token']
                    mailid = request.data["email"]
                    email = EmailMessage()
                    email.subject = "Password Reset at unlabel"
                    email.content_subtype = "html"
                    email.body = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><META http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
                                        <body>
                                        <br><br>
                                        You're receiving this email because you requested a password reset for your Influencer account in the Unlabel App.
                                        <br><br>
                                        Please go to the following page and choose a new password:
                                        <br><br>
                                        """ + tosend + """
                                        <br><br>
                                        Thanks for using our site!
                                        <br/>
                                        <br/>
                                        <p style='font-size:11px;'><i>*** This is a system generated email; Please do not reply. ***</i></p>
                                        </body>
                                        </head>
                                        </html>"""
                    email.from_email = "Unlabel App"
                    email.to = [mailid]
                    email.send()
                    return Response({'code': 'OK'}, status.HTTP_200_OK)
                except:
                    return Response({'code': 'Please try again later'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {"message": "email does not exist"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

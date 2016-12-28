from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.mail import EmailMessage
# from accounts.models import EmailConfirmation


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password','first_name']

    # email = serializers.EmailField(required=True)
    # username = serializers.CharField(required=True,max_length=30)
    # password = serializers.CharField(required=True,max_length=25)

    def create(self, validated_data):
        # customer=User.objects.create_user(validated_data["email"][0:29],validated_data["email"],validated_data["password"])
        # customer.first_name = validated_data["first_name"]

        customer = User.objects.create()
        customer.email = validated_data["email"]
        customer.username = validated_data["email"][0:29]
        customer.set_password(validated_data["password"])
        customer.first_name = validated_data["first_name"]
        customer.save()

        return customer

# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#
#     def validate(self, attrs):
#         email = attrs.get('email')
#         try:
#             user = User.objects.get(email=email)
#             attrs['user'] = user
#         except Exception as e:
#             print(e)
#             raise ValidationError('Email does\'t exist')
#
#         return attrs
#
#     def create(self, validated_data):
#         email = validated_data['email']
#         key = self.generate_hash_key()
#         email_obj = EmailConfirmation()
#         email_obj.key = key
#         email_obj.email = email
#         email_obj.save()
#         self.send_activate_link(validated_data['user'])
#
#         return email_obj
#
#     def send_activate_link(self,user_obj):
#           # Send email with a key
#           key = self.generate_hash_key()
#           # generating confirmation link to be send to user using hash_key
#           link = self.generate_link(key)
#
#           t = loader.get_template('accounts/email_templates/forgotpassword.html')
#           site = Site.objects.get_current()
#           c = Context({'user': user_obj, 'link': link, 'site': site.name})
#           email = EmailMessage('Please Activate Your account', t.render(c), settings.EMAIL_HOST_USER, (user_obj.email, ))
#           email.content_subtype = 'html'
#           email.send()
#
#     def generate_hash_key(self):
#         hash_key = hexlify(os.urandom(15))
#         return hash_key
#
#
#     def generate_link(self,key):
#         url = '/forgot-password/'+str(key)+'/'
#         current_site = Site.objects.get_current()
#         url = current_site.domain + url
#         return url
#

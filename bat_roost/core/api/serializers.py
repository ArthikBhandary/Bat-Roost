from rest_framework import serializers

# from rest_auth.serializers import LoginSerializer
from rest_auth.registration.serializers import RegisterSerializer

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import authenticate
from core.models import User

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', "is_verified", 'contact_no', 'locality')
        read_only_fields = ("pk", "username", "email", "is_verified")


# # class LoginApiSerializers(LoginSerializer):
#
#     def authenticate(self, **kwargs):
#         auth =  authenticate(self.context['request'], **kwargs)
#         return auth



class RegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)
    contact_no = serializers.CharField(required=False, max_length=12)
    locality = serializers.CharField(required=False, max_length=255)

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'contact_no': self.validated_data.get('first_name', ''),
            'locality': self.validated_data.get('last_name', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

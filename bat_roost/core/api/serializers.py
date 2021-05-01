from rest_framework import serializers

from rest_auth.serializers import LoginSerializer
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import authenticate
from core.models import User

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', "is_verified")
        read_only_fields = ("pk", "username", "email", "is_verified")


class LoginApiSerializers(LoginSerializer):

    def authenticate(self, **kwargs):
        auth =  authenticate(self.context['request'], **kwargs)

        raise ValidationError(
            _("Email is not Verified"),
            code="unverified",
        )

        return auth

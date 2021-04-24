from rest_framework import serializers

from core.models import User

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', "is_verified")
        read_only_fields = ("pk", "username", "email", "is_verified")

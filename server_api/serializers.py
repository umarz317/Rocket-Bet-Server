from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pid", "wallet_address", "user_email","user_name", "is_active", "password"]


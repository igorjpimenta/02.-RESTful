from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer as JWTTokenRefreshSerializer
from django.contrib.auth import authenticate
from typing import Dict, Any
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'email', 'name']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            request = self.context.get('request')
            user = authenticate(request=request, email=email, password=password)  # type: ignore

            if not user:
                raise serializers.ValidationError("Invalid login credentials.")

        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        data['user'] = user

        return data


class TokenRefreshSerializer(JWTTokenRefreshSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh = self.token_class(attrs["refresh"])

        data = {
            "access": str(refresh.access_token),
            "access_exp": str(refresh.access_token.payload['exp'])
        }

        return data

from dj_rest_auth.serializers import LoginSerializer, PasswordChangeSerializer
from rest_framework import serializers

from users.models import User, Role


class UserLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs


class UserPasswordChangeSerializer(PasswordChangeSerializer):
    set_password_form_class = 'CustomSetPasswordForm'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        return self.create(self.validated_data)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data, role=Role.objects.get(role='user'), username=validated_data.get('email'))


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']
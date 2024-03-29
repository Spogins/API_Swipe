from datetime import timedelta

from allauth.account.models import EmailAddress
from dj_rest_auth.serializers import LoginSerializer, PasswordChangeSerializer
from django.utils import timezone
from django.utils.encoding import force_str
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import Serializer

from users.forms import CustomSetPasswordForm
from users.models import *


class UerEmailCheckSerializer(serializers.Serializer):
    email = serializers.CharField()


class UserLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs


class UserPasswordChangeSerializer(PasswordChangeSerializer):
    set_password_form_class = CustomSetPasswordForm


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirm_password']

    def save(self, *args, **kwargs):
        return self.create(self.validated_data)

    def create(self, validated_data):
        password = validated_data.get('password')
        confirm_password = validated_data.pop('confirm_password', None)
        if confirm_password:
            if password == confirm_password and len(password) >= 5:
                user = User.objects.create_user(**validated_data, role=Role.objects.get(role='user'), username=validated_data.get('email'))
                return user
            else:
                raise ValidationError(detail={'psw': _('incorrect value')}, code=status.HTTP_400_BAD_REQUEST)
        else:
            raise ValidationError(detail={'psw': _('incorrect value')}, code=status.HTTP_400_BAD_REQUEST)


class BuilderRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirm_password']

    def save(self, *args, **kwargs):
        return self.create(self.validated_data)

    def create(self, validated_data):
        password = validated_data.get('password')
        confirm_password = validated_data.pop('confirm_password', None)
        if confirm_password:
            if password == confirm_password and len(password) >= 5:
                user = User.objects.create_user(**validated_data, role=Role.objects.get(role='builder'), username=validated_data.get('email'))
                return user
            else:
                raise ValidationError(detail={'psw': _('incorrect value')}, code=status.HTTP_400_BAD_REQUEST)
        else:
            raise ValidationError(detail={'psw': _('incorrect value')}, code=status.HTTP_400_BAD_REQUEST)


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        exclude = ['id']


class UserApi64Serializer(serializers.ModelSerializer):
    avatar = Base64ImageField(use_url=True, required=False)

    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser', 'is_staff', 'groups', 'user_permissions', 'is_active']

    def validate_password(self, value: str):
        if len(value) < 5:
            raise ValidationError(detail={'psw': _('incorrect value')}, code=status.HTTP_400_BAD_REQUEST)
        return value

    def update(self, instance: User, validated_data):
        password = validated_data.pop('password', None)

        for field in validated_data.keys():

            if field == 'email' and validated_data.get('email') != instance.email:
                instance.username = validated_data.get('email')
                email_address = EmailAddress.objects.get(user=instance)
                email_address.email = validated_data.get('email')
                email_address.save()

            setattr(instance, field, validated_data.get(field))

        if password:
            instance.set_password(password)

        instance.save()

        return instance


class UserApiSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser', 'is_staff', 'groups', 'user_permissions', 'is_active']

    def validate_password(self, value: str):
        if len(value) < 5:
            raise ValidationError(detail={'psw': _('incorrect value')}, code=status.HTTP_400_BAD_REQUEST)
        return value

    def update(self, instance: User, validated_data):
        password = validated_data.pop('password', None)

        for field in validated_data.keys():

            if field == 'email' and validated_data.get('email') != instance.email:
                instance.username = validated_data.get('email')
                email_address = EmailAddress.objects.get(user=instance)
                email_address.email = validated_data.get('email')
                email_address.save()

            setattr(instance, field, validated_data.get(field))

        if password:
            instance.set_password(password)

        instance.save()

        return instance


class UserAdminApiSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(use_url=True, required=False)

    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser', 'is_staff', 'groups', 'user_permissions', 'date_joined', 'is_active']

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data, username=validated_data.get('email'))
        except:
            raise ValidationError(detail={'psw': _('incorrect value')}, code=status.HTTP_400_BAD_REQUEST)

        EmailAddress.objects.create(
            email=user.email,
            verified=True,
            primary=True,
            user=user
        )

        return user


class NotaryApiSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(use_url=True, required=False)

    class Meta:
        model = Notary
        fields = '__all__'


class MessageApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['text', 'recipient']

    def create(self, validated_data):
        message = Messages.objects.create(
            sender=self.context.get('user'),
            **validated_data
        )
        return message


class SavedFiltersApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedFilters
        exclude = ["user"]

    def create(self, validated_data):
        _filter = SavedFilters.objects.create(
            user=self.context.get('user'),
            **validated_data
        )
        return _filter


class SubscriptionApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class UserSubscriptionSerializer(serializers.ModelSerializer):
    subscription = SubscriptionApiSerializer()

    class Meta:
        model = UserSubscription
        exclude = ['user']
        read_only_fields = ['expire_date']

    def to_internal_value(self, data):
        ret = {}
        try:
            ret['subscription'] = Subscription.objects.get(pk=data.get('subscription'))
        except Subscription.DoesNotExist:
            raise ValidationError({'detail': _('Вказаної підписки не існує.')})
        return ret

    def validate(self, attrs):
        if not self.instance and UserSubscription.objects.filter(user=self.context.get('user')).exists():
            raise ValidationError({'user': _('У вас вже є підписка.')})
        return super().validate(attrs)

    def create(self, validated_data):
        subscription = UserSubscription.objects.create(
            user=self.context.get('user'),
            expire_date=timezone.now() + timedelta(days=30),
            **validated_data
        )
        return subscription

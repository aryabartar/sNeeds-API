import datetime

from django.utils import timezone
from django.core import exceptions
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validators

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import UserInformation

User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA


class UserInformationSerializer(serializers.ModelSerializer):

    def validate_phone(self, phone):
        if not len(phone) == 11:
            raise serializers.ValidationError("Phone length should be 11 characters.")
        try:
            int(phone)
        except:
            raise serializers.ValidationError("Phone should be integer.")
        return phone

    class Meta:
        model = UserInformation
        fields = [
            'phone', 'field', 'university',
        ]
        extra_kwargs = {
            'user': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]
        read_only_fields = ("username", "email",)


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={
        "input_type": 'password'
    }, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    token_expires = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2',
            'token',
            'token_expires',
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_token_expires(self, user):
        return timezone.now() + \
               expire_delta - \
               datetime.timedelta(seconds=200)  # For possible delays

    def get_token(self, user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists  .")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this username exists  . ")
        return value

    def validate(self, data):
        password = data['password']
        password2 = data['password2']
        data.pop('password2')

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        # user.is_active=False #Enable this for email verification
        user.save()
        return user


class PasswordSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={
        "input_type": 'password'
    }, write_only=True)

    class Meta:
        model = User
        fields = ["password", "password2"]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    # def create(self, validated_data):
        
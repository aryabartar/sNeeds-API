import datetime

from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import UserInformation

User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA

User = get_user_model()


class UserInformation(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        fields = [
            "user",
            "phone",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={
        "input_type": 'password'
    }, write_only=True)
    phone = serializers.CharField(max_length=11, min_length=11, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    token_expires = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'password',
            'password2',
            'token',
            'token_expires',
            'message',
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_message(self, user):
        return "Success!"

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
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this username exists.")
        return value

    def validate(self, data):
        password = data['password']
        password2 = data['password2']
        data.pop('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords must match!")

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

        # TODO: Validate this
        # Save user information here
        phone = validated_data['phone']
        UserInformation.objects.create(user=user, phone=phone)
        return user

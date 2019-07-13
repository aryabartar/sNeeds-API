from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validators
from django.core import exceptions

from rest_framework import serializers
from rest_framework_jwt import utils as jwt_utils

from .utils import jwt_response_payload_handler

User = get_user_model()


def validate_user_password(password):
    try:
        # validate the password and catch the exception
        validators.validate_password(password)

    # the exception raised here is different than serializers.ValidationError
    except exceptions.ValidationError as e:
        raise serializers.ValidationError(e.messages)


def validate_email(email):
    qs = User.objects.filter(email__iexact=email)
    if qs.exists():
        raise serializers.ValidationError("User with this email already exists")


def validate_phone_number(phone):
    if len(phone) > 11:
        raise serializers.ValidationError("Phone number is more than 11 characters")
    if len(phone) < 10:
        raise serializers.ValidationError("Phone number is less than 10 characters")


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'address',
            'password',
            'password2',
        ]
        extra_kwargs = {
            'email': {'read_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'address': {'required': False},
            'password': {'write_only': True, 'required': False},
        }

    def validate(self, data):
        pw = data.get('password', -1)
        pw2 = data.get('password2', -1)

        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")

        try:
            data.pop('password2')
        except:
            pass

        return data

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        try:
            password = validated_data.pop('password')
        except:
            pass

        User().update_instance(instance, **validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token_response = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
            'phone_number',
            'address',
            'token_response',
        ]

        extra_kwargs = {'password': {'write_only': True}, }

    def get_token_response(self, obj):  # instance of the model
        user = obj
        payload = jwt_utils.jwt_payload_handler(user)
        token = jwt_utils.jwt_encode_handler(payload)
        response = jwt_response_payload_handler(token, user)
        return response

    def validate_password(self, value):
        validate_user_password(value)
        return value

    def validate_email(self, value):
        validate_email(value)
        return value

    def validate_phone_number(self, value):
        validate_phone_number(value)
        return value

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_obj = User(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
            address=validated_data.get('address'),
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj

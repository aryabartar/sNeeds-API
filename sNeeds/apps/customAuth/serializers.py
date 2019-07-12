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


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token_response = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'password2',
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
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_obj = User(
            email=validated_data.get('email'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj

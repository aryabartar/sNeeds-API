from django.utils.translation import gettext as _

import django.contrib.auth.password_validation as validators
from django.contrib.auth import get_user_model
from django.core import exceptions

from rest_framework import serializers
from rest_framework_jwt import utils as jwt_utils

from ..consultants.serializers import ShortConsultantProfileSerializer
from sNeeds.apps.customAuth.models import UserTypeChoices
from ..consultants.models import ConsultantProfile
from .utils import jwt_response_payload_handler
from .fields import EnumField

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
        raise serializers.ValidationError(_("User with this email already exists"))


def validate_phone_number(phone):
    try:
        int(phone)
    except ValueError:
        raise serializers.ValidationError(_("Phone number should be number only"))


class UserRegisterSerializer(serializers.ModelSerializer):
    token_response = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'phone_number',
            'token_response',
        ]

        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'required': True}
        }

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

    def create(self, validated_data):
        user_obj = User(
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            user_type=1,  # Only student can register with serializer
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
        ]
        extra_kwargs = {
            'email': {'read_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'password': {'write_only': True, 'required': False},
        }

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


class SafeUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = [
            'id',
            'first_name',
            'last_name',
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': False},
        }


class MyAccountSerializer(serializers.ModelSerializer):
    consultant = serializers.SerializerMethodField()
    user_type = EnumField(enum=UserTypeChoices)

    class Meta:
        model = User

        fields = [
            'id',
            'user_type',
            'consultant',
        ]

    def get_consultant(self, obj):
        try:
            consultant = ConsultantProfile.objects.get(user=obj)
            return ShortConsultantProfileSerializer(consultant, context={"request":self.context.get('request')}).data
        except ConsultantProfile.DoesNotExist:
            return None


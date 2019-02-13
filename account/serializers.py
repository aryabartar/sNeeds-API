from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={
        "input_type": 'password'
    }, write_only=True)

    password2 = serializers.CharField(style={
        "input_type": 'password'
    }, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

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
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

from rest_framework import serializers

from . import models

User = get_user_model()


def validate_user_password(password):
    try:
        # validate the password and catch the exception
        validators.validate_password(password)

    # the exception raised here is different than serializers.ValidationError
    except exceptions.ValidationError as e:
        raise serializers.ValidationError(e.messages)


class CountrySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="account:country-detail", lookup_field='slug', read_only=True)

    class Meta:
        model = models.Country
        fields = ('url', 'name', 'slug')


class UniversitySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="account:university-detail", lookup_field='slug',
                                               read_only=True)

    class Meta:
        model = models.University
        fields = ('url', 'name', 'country', 'description', 'slug')


class FieldOfStudySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="account:field-of-study-detail", lookup_field='slug',
                                               read_only=True)

    class Meta:
        model = models.FieldOfStudy
        fields = ('url', 'name', 'description', 'slug')


class ConsultantProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:consultant-profile-detail",
        lookup_field='slug',
        read_only=True
    )

    universities = UniversitySerializer(many=True, read_only=True)
    field_of_studies = FieldOfStudySerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = models.ConsultantProfile
        fields = ('url', 'pk', 'user', 'universities', 'field_of_studies', 'countries', 'slug', 'aparat_link')


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

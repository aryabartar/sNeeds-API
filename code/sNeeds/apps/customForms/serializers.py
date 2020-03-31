from rest_framework.serializers import ModelSerializer
from .models import BugReport, PackageForm


class BugReportSerializer(ModelSerializer):

    class Meta:
        model = BugReport
        fields = [
            'id',
            'picture',
            'comment',
            'email',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        if validated_data.get('email', "") == "" and user.is_authenticated:
            validated_data['email'] = user.email
        return super(BugReportSerializer, self).create(validated_data)


class PackageFormSerializer(ModelSerializer):

    class Meta:
        model = PackageForm
        fields = '__all__'
        exclude = ('user',)

        extra_kwargs = {
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        package_form_obj = PackageForm.objects.create(user=user, **validated_data)
        return package_form_obj

from rest_framework.serializers import ModelSerializer
from .models import BugReport


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
        if user.is_authenticated:
            validated_data['email'] = user.email
        return super(BugReportSerializer, self).create(validated_data)

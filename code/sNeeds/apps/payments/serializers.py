from rest_framework.serializers import ModelSerializer
from sNeeds.apps.payments.models import ConsultantDepositInfo


class ConsultantDepositInfoSerializer(ModelSerializer):

    class Meta:
        model = ConsultantDepositInfo
        fields = ['id', 'tracing_code', 'amount', 'updated', 'comment']

        extra_kwargs = {
            'id': {'read_only': True},
            'tracing_code': {'read_only': True},
            'amount': {'read_only': True},
            'updated': {'read_only': True},
            'comment': {'read_only': True},
        }

from rest_framework.serializers import ModelSerializer
from sNeeds.apps.payments.models import ConsultantDepositInfo


class ConsultantDepositInfoSerializer(ModelSerializer):

    class Meta:
        model = ConsultantDepositInfo
        fields = ['consultant_deposit_info_id', 'amount', 'updated', 'comment']

        extra_kwargs = {
            'consultant_deposit_info_id': {'read_only': True},
            'amount': {'read_only': True},
            'updated': {'read_only': True},
            'comment': {'read_only': True},
        }

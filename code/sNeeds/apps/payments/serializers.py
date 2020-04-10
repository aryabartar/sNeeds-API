from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from sNeeds.apps.payments.models import ConsultantDepositInfo


class ConsultantDepositInfoSerializer(ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        source='payments',
        lookup_field='consultant_deposit_info_id',
        read_only=True,
        view_name='payment:consultant-deposit-detail'
    )
    
    class Meta:
        model = ConsultantDepositInfo
        fields = ['consultant_deposit_info_id', 'amount', 'updated', 'comment', 'url']

        extra_kwargs = {
            'consultant_deposit_info_id': {'read_only': True},
            'amount': {'read_only': True},
            'updated': {'read_only': True},
            'comment': {'read_only': True},
        }

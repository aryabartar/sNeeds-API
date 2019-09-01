from django.core.exceptions import ValidationError
from django.utils import timezone

from rest_framework import serializers

from .models import TimeSlotSale, SoldTimeSlotSale

from sNeeds.apps.account.models import ConsultantProfile
from sNeeds.apps.account.serializers import ConsultantProfileSerializer, ShortConsultantProfileSerializer
from sNeeds.apps.customAuth.serializers import SafeUserDataSerializer

import datetime


class TimeSlotSaleSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(read_only=True, lookup_field='id',
	                                           view_name="store:time-slot-sale-detail")

	consultant_url = serializers.HyperlinkedRelatedField(
		source='consultant',
		lookup_field='slug',
		read_only=True,
		view_name='account:consultant-profile-detail'
	)

	consultant = serializers.SerializerMethodField()

	class Meta:
		model = TimeSlotSale
		fields = (
			'id', 'url', 'consultant', 'consultant_url', 'start_time', 'end_time',
			'price',)

		extra_kwargs = {
			'id': {'read_only': True},
			'consultant': {'read_only': True}
		}

	def get_consultant(self, obj):
		request = self.context.get('request')

		return ShortConsultantProfileSerializer(
			obj.consultant, context={'request': request}
		).data

	def create(self, validated_data):
		request = self.context.get('request', None)
		user = request.user
		consultant_profile = ConsultantProfile.objects.get(user=user)

		obj = TimeSlotSale.objects.create(
			consultant=consultant_profile,
			start_time=validated_data['start_time'],
			end_time=validated_data['end_time'],
			price=validated_data['price'],
		)

		return obj

	def validate_start_time(self, obj):
		if obj < (timezone.now() + datetime.timedelta(days=1)):
			raise ValidationError(
				"Start time should be selected at least "
				"from a day after today."
			)
		return obj

	def validate(self, data):
		if data['start_time'] >= data['end_time']:
			raise serializers.ValidationError("finish must occur after start")
		return data


class SoldTimeSlotSaleSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(
		view_name="store:sold-time-slot-sale-detail",
		lookup_field='id',
		read_only=True
	)

	consultant = serializers.SerializerMethodField()
	sold_to = serializers.SerializerMethodField()

	class Meta:
		model = SoldTimeSlotSale
		fields = [
			'id', 'url', 'consultant', 'start_time', 'end_time',
			'price', 'sold_to', 'used',
		]

	def get_sold_to(self, obj):
		return SafeUserDataSerializer(obj.sold_to).data

	def get_consultant(self, obj):
		request = self.context.get('request')

		return ShortConsultantProfileSerializer(
			obj.consultant, context={'request': request}
		).data

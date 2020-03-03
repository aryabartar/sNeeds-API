from django.utils.translation import gettext as _

from rest_framework import serializers

from sNeeds.apps.customAuth.models import ConsultantProfile

from .models import TMPConsultant



class ConsultantSerializer(serializers.ModelSerializer):

    class Meta:
        model = TMPConsultant
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'university',
            'field_of_study',
            'resume',
        ]

    def validate_phone_number(self, value):
        if ConsultantProfile.objects.filter(user__phone_number=value).count() > 0:
            raise serializers.ValidationError(_("A Consultant with this phone number exists. Are you not a Consultant?"))
        if TMPConsultant.objects.filter(phone_number=value).count() > 0:
            raise serializers.ValidationError(_("A Consultant with phone number is in assessment."))
        if len(value) != 11:
            raise serializers.ValidationError(_("Phone number should be 11 numbers"))
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError(_("Phone number should be numbers."))
        return value

    def validate_email(self, value):
        if ConsultantProfile.objects.filter(user__email=value).count() > 0:
            raise serializers.ValidationError(_("A Consultant with this email exists. Are you not a Consultant?"))
        if TMPConsultant.objects.filter(email=value).count() > 0:
            raise serializers.ValidationError(_("A Consultant with this email is in assessment."))
        return value

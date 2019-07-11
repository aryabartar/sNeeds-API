from django_filters import rest_framework as filters

from . import models
from sNeeds.apps.account.models import ConsultantProfile


class TimeSlotSailFilter(filters.FilterSet):
    consultant = filters.ModelMultipleChoiceFilter(field_name='consultant', to_field_name='slug',
                                                          queryset=ConsultantProfile.objects.all(), label="slug")

    class Meta:
        model = models.TimeSlotSale
        fields = ['consultant', 'start_time', 'end_time', 'price']

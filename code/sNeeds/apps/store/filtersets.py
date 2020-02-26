from django_filters import rest_framework as filters, DateTimeFromToRangeFilter

from . import models

from sNeeds.utils.custom.filterset import CustomDateTimeFromToRangeFilter


class TimeSlotSaleFilter(filters.FilterSet):
    price = filters.RangeFilter(field_name="price")

    start_time_range = CustomDateTimeFromToRangeFilter(field_name="start_time")
    end_time_range = CustomDateTimeFromToRangeFilter(field_name="end_time")

    class Meta:
        model = models.TimeSlotSale
        fields = [
            'consultant', 'start_time_range', 'end_time_range',
            'price'
        ]

from django_filters import rest_framework as filters, DateTimeFromToRangeFilter

from . import models


class TimeSlotSaleFilter(filters.FilterSet):
    price = filters.RangeFilter(field_name="price")

    class Meta:
        model = models.TimeSlotSale
        fields = [
            'consultant', 'price', 'start_time', 'end_time'
        ]

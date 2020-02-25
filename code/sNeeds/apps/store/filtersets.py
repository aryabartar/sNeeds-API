from django_filters import rest_framework as filters

from . import models


class TimeSlotSaleFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    min_start_time = filters.DateTimeFilter(field_name="start_time", lookup_expr="gte")
    max_start_time = filters.DateTimeFilter(field_name="start_time", lookup_expr="lte")

    min_end_time = filters.DateTimeFilter(field_name="end_time", lookup_expr="gte")
    max_end_time = filters.DateTimeFilter(field_name="end_time", lookup_expr="lte")

    class Meta:
        model = models.TimeSlotSale
        fields = [
            'consultant', 'min_start_time', 'max_start_time',
            'min_end_time', 'max_end_time',
            'end_time', 'min_price', 'max_price', 'price'
        ]

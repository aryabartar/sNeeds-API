from django_filters import rest_framework as filters

from . import models


class TimeSlotSaleFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = models.TimeSlotSale
        fields = ['consultant', 'start_time', 'end_time', 'min_price', 'max_price', 'price']

import django_filters
from django.forms import DateTimeField


class CustomDateTimeRangeField(django_filters.filters.RangeField):
    widget = django_filters.filters.DateTimeRangeField.widget

    def __init__(self, *args, **kwargs):
        fields = (
            DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%SZ']),
            DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%SZ']),
        )
        super(CustomDateTimeRangeField, self).__init__(fields, *args, **kwargs)


class CustomDateTimeFromToRangeFilter(django_filters.RangeFilter):
    field_class = CustomDateTimeRangeField


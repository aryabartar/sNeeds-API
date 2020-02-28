from django_filters import rest_framework as filters

from . import models


class CommentFilterSet(filters.FilterSet):
    time_range = filters.IsoDateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = models.ConsultantComment
        fields = ['user', 'consultant', 'time_range', ]

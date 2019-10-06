from django_filters import rest_framework as filters

from . import models


class CommentFilterSet(filters.FilterSet):
    time_range = filters.IsoDateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = models.Comment
        fields = ['user', 'consultant', 'time_range', ]


class AdminCommentFilterSet(filters.FilterSet):
    time_range = filters.IsoDateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = models.AdminComment
        fields = ['comment', 'time_range', ]

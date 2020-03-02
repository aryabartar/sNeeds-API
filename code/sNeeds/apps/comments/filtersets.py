from django_filters import rest_framework as filters

from . import models


class CommentFilterSet(filters.FilterSet):

    class Meta:
        model = models.ConsultantComment
        fields = ['user', 'consultant', ]

from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import BookletField, BookletTopic, Booklet
from .serializers import FieldSerializer, TopicSerializer


class GetFieldsList(APIView):
    def get(self, request):
        all_fields = BookletField.objects.all()
        serialize_fields = FieldSerializer(all_fields, many=True)
        return Response(serialize_fields.data)


class GetField(APIView):
    def get(self, request, field_slug):
        field = BookletField.objects.get(slug__exact=field_slug)
        return Response(FieldSerializer(field).data)

from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import BookletField, BookletTopic, Booklet
from .serializers import FieldSerializer, TopicSerializer, BookletSerializer


class GetFieldsList(APIView):
    def get(self, request):
        all_fields = BookletField.objects.all()
        serialize_fields = FieldSerializer(all_fields, many=True, context={'request': request})
        return Response(serialize_fields.data)


class GetField(APIView):
    def get(self, request, field_slug):
        field = BookletField.objects.get(slug__exact=field_slug)
        field_serialize = FieldSerializer(field, context={"request": request})
        return Response(field_serialize.data)


class GetTopic(APIView):
    def get(self, request, field_slug, topic_slug):
        topic = BookletTopic.objects.get(slug__exact=topic_slug, field__slug__exact=field_slug)
        topic_serialize = TopicSerializer(topic, context={'request': request})
        return Response(topic_serialize.data)


class GetBooklet(APIView):
    def get(self, request, field_slug, topic_slug, booklet_slug):
        booklet = Booklet.objects.get(slug__exact=booklet_slug,
                                      topic__slug__exact=topic_slug,
                                      topic__field__slug__exact=field_slug, )
        booklet_serialize = BookletSerializer(booklet, context={'request': request})
        print(booklet_serialize.data)
        return Response(booklet_serialize.data)

from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import BookletField, BookletTopic, Booklet, Tag
from .serializers import FieldSerializer, TopicSerializer, BookletSerializer


class FieldsList(APIView):
    def get(self, request):
        all_fields = BookletField.objects.all()
        serialize_fields = FieldSerializer(all_fields, many=True, context={'request': request})
        return Response(serialize_fields.data)


class FieldsDetail(APIView):
    def get(self, request, field_slug):
        field = BookletField.objects.get(slug__exact=field_slug)
        field_serialize = FieldSerializer(field, context={"request": request})
        return Response(field_serialize.data)


class FieldTopicsList(APIView):
    def get(self, request, field_slug):
        field = BookletField.objects.get(slug__exact=field_slug)
        topic = field.topics.all()
        topic_serializer = TopicSerializer(topic, many=True, context={"request": request})
        return Response(topic_serializer.data)


class TopicsList(APIView):
    def get(self, request):
        topics = BookletTopic.objects.all()
        topics_serialize = TopicSerializer(topics, many=True, context={"request": request})
        return Response(topics_serialize.data)


class TopicsDetail(APIView):
    def get(self, request, topic_slug):
        topic = BookletTopic.objects.get(slug__exact=topic_slug)
        topic_serialize = TopicSerializer(topic, context={"request": request})
        return Response(topic_serialize.data)


class TopicBookletsList(APIView):
    def get(self, request, topic_slug):
        topic = BookletTopic.objects.get(slug__exact=topic_slug)
        booklets = topic.booklets
        booklet_serialize = BookletSerializer(booklets, many=True, context={"request": request})
        return Response(booklet_serialize.data)


class BookletsList(APIView):
    def get(self, request):
        booklets = Booklet.objects.all()
        booklet_serialize = BookletSerializer(booklets, many=True, context={"request": request})
        return Response(booklet_serialize.data)


# class BookletDetail(APIView):
#     def get(self, request):
#         b
#
# class GetTopic(APIView):
#     def get(self, request, field_slug, topic_slug):
#         topic = BookletTopic.objects.get(slug__exact=topic_slug, field__slug__exact=field_slug)
#         topic_serialize = TopicSerializer(topic, context={'request': request})
#         return Response(topic_serialize.data)
#
#
# class GetBooklet(APIView):
#     def get(self, request, field_slug, topic_slug, booklet_slug):
#         booklet = Booklet.objects.get(slug__exact=booklet_slug,
#                                       topic__slug__exact=topic_slug,
#                                       topic__field__slug__exact=field_slug, )
#         # TODO: Better way
#         try:
#             if request.GET['like'] == 'true':
#                 booklet.number_of_likes += 1
#                 booklet.save()
#         except:
#             pass
#
#         booklet_serialize = BookletSerializer(booklet, context={'request': request})
#         return Response(booklet_serialize.data)
#
#
# class TagsList(APIView):
#     def get(self, request):
#         tags = Tag.objects.all()
#         tags_serialize = TagSerializer(tags, many=True, context={"request": request})
#         return Response(tags_serialize.data)
#
#
# class TagsDetail(APIView):
#     def get(self, request, tag_slug):
#         tag = get_object_or_404(Tag, slug=tag_slug)
#         tag_serialize = TagSerializer(tag, context={"request": request})
#         return Response(tag_serialize.data)
#
#
# class TagsPostsList(generics.ListAPIView):
#     serializer_class = BookletSerializer
#     queryset = Booklet.objects.all()
#     pagination_class = LimitOffsetPagination
#
#     def get_queryset(self):
#         tag_slug = self.kwargs["tag_slug"]
#         tag = get_object_or_404(Tag, slug=tag_slug)
#         booklets = tag.booklets.all()
#         return booklets

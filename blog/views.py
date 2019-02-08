from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import (
    Post,
    UserComment,
    Topic,
)

from .serializers import (
    PostSerializer,
    UserCommentSerializer,
    TopicSerializer,
)


# Create your views here.
class PostPages(generics.ListAPIView):
    def __init__(self):
        import os
        import django

        os.environ['DJANGO_SETTINGS_MODULE'] = 'sneeds.settings.production'

        django.setup()

        from blog.models import Topic, Post, UserComment, AdminComment
        from faker import Faker
        from random import randint

        fake = Faker()



        all_comments = UserComment.objects.all()
        all_comments_number = len(all_comments)

        for i in range(0, all_comments_number // 2):
            try:
                content = "من ادمینم و مثلا بهت یه جواب دادم. ایول که اومدی کامنت گذاشتی. خیلی حال دادی"
                comment = all_comments[randint(0, all_comments_number - 1)]
                obj = AdminComment(content=content, user_comment=comment)
                obj.save()
            except:
                pass


    permission_classes = []
    authentication_classes = []
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = LimitOffsetPagination


class CreateUserComment(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = UserComment.objects.all()
    serializer_class = UserCommentSerializer


class TopicDetail(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        topic_slug = self.kwargs['topic_slug']
        qs = Post.objects.filter(topic__slug=topic_slug)
        return qs


class PostDetail(APIView):
    serializer_class = UserCommentSerializer

    def get(self, request, post_slug, topic_slug):
        post = Post.objects.get(slug=post_slug, topic__slug=topic_slug)
        post_serialize = PostSerializer(post, context={"request": request})
        return Response(data=post_serialize.data)

    def post(self, request, post_slug, topic_slug):
        comment_serialize = UserCommentSerializer(data=request.data)
        if comment_serialize.is_valid():
            comment_serialize.save()
            return Response(comment_serialize.data)
        else:
            return Response(comment_serialize.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicList(generics.ListAPIView):
    """
    Returns all topics as a list
    """
    permission_classes = []
    authentication_classes = []
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

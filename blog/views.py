from rest_framework import generics, mixins, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import (
    Post,
    UserComment,
    Topic,
    PostLike,
)

from .serializers import (
    PostSerializer,
    UserCommentSerializer,
    TopicSerializer,
    PostLikeSerializer,
)


# Create your views here.
class PostPages(generics.ListAPIView):
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


def get_post(post_slug):
    post = None
    posts = Post.objects.filter(slug__iexact=post_slug)
    if posts.count() == 1:
        post = posts.first()
    return post


class TopicList(generics.ListAPIView):
    """
    Returns all topics as a list
    """
    permission_classes = []
    authentication_classes = []
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class PostLikesList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        post = get_post(kwargs["post_slug"])

        if user.is_authenticated:
            likes = user.likes.all()
            for like in likes:
                if like.post == post:
                    return Response({"liked": "true"})
            return Response({"liked": "false"})
        return Response({"message": "User is not authenticated."})

    def post(self, request, *args, **kwargs):
        user = request.user
        post = get_post(kwargs["post_slug"])

        if user.is_authenticated:
            try:
                PostLike.objects.create(user=user, post=post)
            # When trying to make duplicate values
            except:
                return Response({"message": "This user already liked this post"})
        else:
            PostLike.objects.create(user=None, post=post)

        return Response({"message": "Success"})

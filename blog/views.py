from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

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
class FirstPage(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        qs = Post.objects.all()
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)


class CreateUserComment(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = UserComment.objects.all()
    serializer_class = UserCommentSerializer


class PostDetail(generics.RetrieveAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # Override get method(default returns 'id')
    def get_object(self):
        """
        Returns post according to 'slug' and 'topic_slug'
        """
        kwargs = self.kwargs
        slug = kwargs.get('post_slug')
        topic_slug = kwargs.get('topic_slug')
        return Post.objects.get(slug=slug, topic__slug=topic_slug)


class TopicDetail(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = PostSerializer

    def get_queryset(self):
        topic_slug = self.kwargs['topic_slug']
        qs = Post.objects.filter(topic__slug=topic_slug)
        return qs
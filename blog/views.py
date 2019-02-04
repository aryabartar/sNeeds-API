from rest_framework import generics
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
    PostCommentsSerializer,
)


# Create your views here.
class PostPages(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = LimitOffsetPagination

class TopicDetail(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        topic_slug = self.kwargs['topic_slug']
        qs = Post.objects.filter(topic__slug=topic_slug)
        return qs


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


class CreateUserComment(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = UserComment.objects.all()
    serializer_class = UserCommentSerializer


class GetPostComments(APIView):
    def get(self, request, *args, **kwargs):
        post_slug = kwargs['post_slug']
        post = Post.objects.get(slug=post_slug)
        user_comments = post.comments.all()

        context = []
        for comment in user_comments:
            admin_comment = None
            try:
                admin_comment = comment.admin_comment.content
            except:
                pass

            dict = {"username": comment.user.username,
                    "comment": comment.content,
                    "admin_name": "اسنیدز",
                    "admin_answer": admin_comment
                    }
            context.append(dict)

        serializer = PostCommentsSerializer(context, many=True)
        return Response(serializer.data)

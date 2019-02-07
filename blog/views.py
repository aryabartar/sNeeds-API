from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from .serializers import HelloSerializer

from .models import (
    Post,
    UserComment,
    Topic,
    HelloModel,
)

from .serializers import (
    PostSerializer,
    UserCommentSerializer,
    TopicSerializer,
    PostCommentsSerializer,
    HelloSerializer,
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


class GetPostComments(generics.CreateAPIView, APIView):
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

    permission_classes = []
    authentication_classes = []
    queryset = UserComment.objects.all()
    serializer_class = UserCommentSerializer


class TopicList(generics.ListAPIView):
    """
    Returns all topics as a list
    """
    permission_classes = []
    authentication_classes = []
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class HelloView(APIView):
    serializer_class = HelloSerializer

    def get(self, request, format=None):
        all_hellos = HelloModel.objects.all()
        print(all_hellos)
        serializer = HelloSerializer(all_hellos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serilize = HelloSerializer(data=request.data)
        if serilize.is_valid():
            return Response({"valid": "hey"})
        else:
            return Response(serilize.errors)
        # return Response(status.HTTP_204_NO_CONTENT)

    def put(self, request, pk=None):
        return Response({"method": "post"})

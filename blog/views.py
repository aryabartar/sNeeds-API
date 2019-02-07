from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django import http

from .models import (
    Post,
    UserComment,
    Topic,
    HelloModel,
)

from .serializers import (
    PostSerializer,
    UserCommentSerializer,
    UserCommentSerializer11,
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


class CreateUserComment(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = UserComment.objects.all()
    serializer_class = UserCommentSerializer


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


class HelloListView(APIView):
    def get(self, request, format=None):
        all_hellos = HelloModel.objects.all()
        serializer = HelloSerializer(all_hellos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HelloSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)


class HelloDetailView(APIView):
    def get_object(self, pk):
        try:
            return HelloModel.objects.get(pk=pk)
        except HelloModel.DoesNotExist:
            raise http.Http404

    def get(self, request, pk, format=None):
        hello = self.get_object(pk)
        serializer = HelloSerializer(hello)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = HelloSerializer(request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    # def delete(self, requset, pk, format=None):
    #     obj = self.get_object(pk)
    #     obj.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

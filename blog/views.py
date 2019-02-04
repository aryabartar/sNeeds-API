from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post, UserComment
from .serializers import PostSerializer, \
    UserCommentSerializer


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

# class PostListView(generics.ListAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#     def get_queryset(self):

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CommentSerializer
from .models import Comment
from .permissions import CommentOwnerPermission


class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentOwnerPermission, permissions.IsAuthenticatedOrReadOnly]

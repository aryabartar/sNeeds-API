from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CommentSerializer
from .models import Comment
from .permissions import CommentOwnerPermission
from .filtersets import CommentFilterSet


class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-created')
    serializer_class = CommentSerializer
    permission_classes = [CommentOwnerPermission, permissions.IsAuthenticatedOrReadOnly]
    filterset_class = CommentFilterSet

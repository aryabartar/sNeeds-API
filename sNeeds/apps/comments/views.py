from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CommentSerializer, AdminCommentSerializer
from .models import Comment, AdminComment
from .permissions import CommentOwnerPermission
from .filtersets import CommentFilterSet, AdminCommentFilterSet


class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-created')
    serializer_class = CommentSerializer
    permission_classes = [CommentOwnerPermission, permissions.IsAuthenticatedOrReadOnly]
    filterset_class = CommentFilterSet


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Comment.objects.all().order_by('-created')
    serializer_class = CommentSerializer
    permission_classes = [CommentOwnerPermission, permissions.IsAuthenticatedOrReadOnly]


class AdminCommentListView(generics.ListAPIView):
    queryset = AdminComment.objects.all().order_by('-created')
    serializer_class = AdminCommentSerializer
    filterset_class = AdminCommentFilterSet

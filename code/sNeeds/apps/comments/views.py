from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, SoldTimeSlotRate
from .serializers import CommentSerializer, SoldTimeSlotRateSerializer
from .permissions import CommentOwnerPermission, SoldTimeSlotRateOwnerPermission
from .filtersets import CommentFilterSet


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


class SoldTimeSlotRateListView(generics.ListCreateAPIView):
    queryset = SoldTimeSlotRate.objects.all()
    serializer_class = SoldTimeSlotRateSerializer
    permission_classes = [SoldTimeSlotRateOwnerPermission, permissions.IsAuthenticatedOrReadOnly]
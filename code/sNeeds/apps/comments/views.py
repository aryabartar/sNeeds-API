from rest_framework import status, generics, mixins, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ConsultantComment, SoldTimeSlotRate
from .serializers import CommentSerializer, SoldTimeSlotRateSerializer
from .filtersets import CommentFilterSet
from ..consultants.models import ConsultantProfile


class CommentListView(generics.ListCreateAPIView):
    queryset = ConsultantComment.objects.all().order_by('-created')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = CommentFilterSet


class CommentDetailView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = ConsultantComment.objects.all()
    serializer_class = CommentSerializer


class SoldTimeSlotRateListView(generics.ListCreateAPIView):
    queryset = SoldTimeSlotRate.objects.all()
    serializer_class = SoldTimeSlotRateSerializer
    filterset_fields = ['sold_time_slot', ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        qs = SoldTimeSlotRate.objects.filter(sold_time_slot__sold_to=user) | \
             SoldTimeSlotRate.objects.filter(sold_time_slot__consultant__user=user)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Changed because previously one object was returned in a list
        if queryset.count() == 1 and self.request.GET.get("sold_time_slot") is not None:
            serializer = self.get_serializer(queryset.first())
        else:
            serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

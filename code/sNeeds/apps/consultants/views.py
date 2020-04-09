from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.consultants.serializers import ConsultantProfileSerializer
from .models import UniversityThrough
# from .filters import ConsultantProfileFilterset


class ConsultantProfileDetail(APIView):
    def get_object(self, slug):
        try:
            return ConsultantProfile.objects.get(slug=slug)
        except ConsultantProfile.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        consultant_profile = self.get_object(slug)
        serializer = ConsultantProfileSerializer(
            consultant_profile,
            context={"request": request}
        )
        return Response(serializer.data)


class ConsultantProfileList(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ConsultantProfileSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    ordering_fields = ['rate', 'created', ]
    filterset_fields = ('universities', 'field_of_studies', 'countries', 'active',)

    def get_queryset(self):
        #TODO: After deploy
        # return ConsultantProfile.objects.get_active_consultants()

        qs = ConsultantProfile.objects.all()
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# class ConsultantProfileList(generics.ListAPIView):
#     serializer_class = ConsultantProfileSerializer
#     pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
#     ordering_fields = ['rate', 'created', ]
#     filterset_fields = ('universities', 'field_of_studies', 'countries', 'active',)
#     # filterset_class = ConsultantProfileFilterset
#
#     def get_queryset(self):
#         #TODO: After deploy
#         # return ConsultantProfile.objects.get_active_consultants()
#         return UniversityThrough.objects.filter_consultants(self.request.query_params)


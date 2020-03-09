from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.consultants.serializers import ConsultantProfileSerializer


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


# TODO: Show consultants based on ...
class ConsultantProfileList(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = ConsultantProfile.objects.all()
    serializer_class = ConsultantProfileSerializer
    ordering_fields = ['rate', 'created', ]
    filterset_fields = ('universities', 'field_of_studies', 'countries', 'active',)

    def get_queryset(self):
        return ConsultantProfile.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

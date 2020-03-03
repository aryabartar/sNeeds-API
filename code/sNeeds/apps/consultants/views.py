from rest_framework import status, generics, mixins, permissions

from .serializers import ConsultantSerializer


class ConsultantCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ConsultantSerializer
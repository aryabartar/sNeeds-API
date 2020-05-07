from django.contrib.auth import authenticate, get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import permissions, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from .serializers import UserRegisterSerializer
from .permissions import NotLoggedInPermission, SameUserPermission

User = get_user_model()


class UserListView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [NotLoggedInPermission]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated'}, status=400)
        return self.create(request, *args, **kwargs)


class UserDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, SameUserPermission]

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs.get('id', None):
            return Response({"detail": "You are not logged in as this user."}, 403)
        return self.retrieve(request)

    def put(self, request, *args, **kwargs):
        if request.user.id != kwargs.get('id', None):
            return Response({"detail": "You are not logged in as this user."}, 403)
        return self.update(request)


class MyAccountInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request):
        my_account = self.get_object()
        serializer = serializers.MyAccountSerializer(my_account, context={"request": request})
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = serializers.CustomTokenObtainPairSerializer

from datetime import datetime

from django.contrib.auth import authenticate, get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, permissions, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt import utils as jwt_utils

from . import serializers
from .utils import jwt_response_payload_handler
from .serializers import UserRegisterSerializer, StudentDetailedInfoSerializer
from .permissions import NotLoggedInPermission, SameUserPermission, StudentDetailedInfoListCreatePermission,\
    StudentDetailedInfoRetrieveUpdatePermission
from .models import StudentDetailedInfo
from ...utils.custom.custom_permissions import CustomIsAuthenticated


User = get_user_model()


class AuthView(APIView):
    permission_classes = [NotLoggedInPermission]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
        }
    ))
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated'}, status=400)

        data = request.data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            payload = jwt_utils.jwt_payload_handler(user)
            token = jwt_utils.jwt_encode_handler(payload)
            response = jwt_response_payload_handler(token, user=user, request=request)

            return Response(response, status=200)

        else:
            return Response({'detail': 'Invalid email/password'}, status=401)


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


class StudentDetailedInfoListCreateAPIView(generics.ListCreateAPIView):
    queryset = StudentDetailedInfo.objects.all()
    serializer_class = StudentDetailedInfoSerializer
    permission_classes = (permissions.IsAuthenticated, StudentDetailedInfoListCreatePermission)

    def get_queryset(self):
        user = self.request.user
        qs = StudentDetailedInfo.objects.filter(user=user)
        return qs


class StudentDetailedInfoRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = StudentDetailedInfo.objects.all()
    serializer_class = StudentDetailedInfoSerializer
    permission_classes = (permissions.IsAuthenticated, StudentDetailedInfoRetrieveUpdatePermission)





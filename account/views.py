from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q

from rest_framework import permissions, generics, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .permissions import AnonPermissionOnly
from .serializers import UserRegisterSerializer, UserSerializer, UserInformationSerializer

from blog.serializers import PostLikeSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class AuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail": "You are already authenticated"}, status=400)

        data = request.data
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        qs = User.objects.filter(
            Q(username__iexact=username_or_email) |
            Q(email__iexact=username_or_email)
        )
        if qs.exists():
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                return Response(response)

        return Response({"detail": "Invalid credentials!"}, status=401)


class RegisterView(APIView):
    def get_created_user(self, username):
        qs = User.objects.filter(username__exact=username)
        if qs.exists():
            user = qs.first()
            return user
        return None

    permission_classes = [AnonPermissionOnly]

    def post(self, request):
        user_register_serialize = UserRegisterSerializer(data=request.data)
        user_information_serialize = UserInformationSerializer(data=request.data)

        user_register_serialize.is_valid()
        user_information_serialize.is_valid()

        if user_register_serialize.is_valid() and user_information_serialize.is_valid():
            user_register_serialize.save()
            user = self.get_created_user(user_register_serialize.data['username'])
            user_information_serialize = UserInformationSerializer(data={**request.data, **{"user": user.pk}})
            if user_information_serialize.is_valid():
                user_information_serialize.save()
            else:
                return Response(user_information_serialize.errors)
            return Response({**user_register_serialize.data, **user_information_serialize.data})
        else:
            return Response({**user_register_serialize.errors, **user_information_serialize.errors})


class MyAccountDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_user_information(self, user):
        try:
            user_information = user.user_information
        except:
            return Response({"This user has no user_information, Please check this first."}, status=400)
        return user_information

    def get(self, request):
        user = request.user
        user_serialize = UserSerializer(request.user)
        user_information = self.get_user_information(user)
        user_information_serialize = UserInformationSerializer(user_information)
        return Response({**user_serialize.data, **user_information_serialize.data})

    def put(self, request):
        user = request.user
        user_serialize = UserSerializer(user, request.data)

        user_information = self.get_user_information(user)
        user_information_serializer = UserInformationSerializer(user_information,
                                                                data={**request.data, **{"user": user.pk}})
        # and in if doesn't check both operands if one of them is false
        user_serialize.is_valid()
        user_information_serializer.is_valid()

        if user_information_serializer.is_valid() and user_serialize.is_valid():
            user_serialize.save()
            user_information_serializer.save()
            return Response({**user_serialize.data, **user_information_serializer.data})
        else:
            return Response({**user_information_serializer.errors, **user_serialize.errors}, status=400)


class AccountLikedPosts(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        likes = user.likes.all()
        if likes.exists():
            post_like_serialize = PostLikeSerializer(likes, many=True)
            return Response(post_like_serialize.data)
        else:
            return Response({"message": "No likes found."})

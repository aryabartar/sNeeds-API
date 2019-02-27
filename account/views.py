from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q

from rest_framework import permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .serializers import UserRegisterSerializer, UserSerializer
from .permissions import AnonPermissionOnly

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
            Q(username__exact=username_or_email) |
            Q(email__exact=username_or_email)
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


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class MyAccountDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_serialize = UserSerializer(request.user)
        return Response(user_serialize.data)

    # def update(self , request):


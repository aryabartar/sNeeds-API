import datetime

from django.contrib.auth import authenticate
from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_jwt import utils as jwt_utils



class AuthView(APIView):
    '''
    Post format:
        {
        "email":"bartararya@gmail.com",
        "password":"****:)"
        }
    '''
    permission_classes = []

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
            response = jwt_utils.jwt_response_payload_handler(token, user=user, request=request)

            expires = {'expires': timezone.now() + settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA'] - datetime.timedelta(seconds=200)}
            response.update(expires)
            return Response(response, status=200)

        else:
            return Response({'detail': 'Invalid email/password'}, status=401)


from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

app_name = "auth"

urlpatterns = [
    path('jwt/token/', obtain_jwt_token),
    path('jwt/token/refresh/', refresh_jwt_token),
]

from django.urls import path

from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

from .views import AuthView


app_name = "auth"

urlpatterns = [
    path('jwt/token/', AuthView.as_view()),
    path('jwt/token/refresh/', refresh_jwt_token),
    path('jwt/token/verify/', verify_jwt_token),

]

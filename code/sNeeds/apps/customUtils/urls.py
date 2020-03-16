from django.urls import path, include

from rest_framework_jwt.views import refresh_jwt_token

from . import views

app_name = "customUtils"

urlpatterns = [
    path('timezone-time/<str:timezone>/', views.TimezoneTimeDetailAPIView.as_view()),
]

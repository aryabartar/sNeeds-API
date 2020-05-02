from django.urls import path, include

from . import views

app_name = "customUtils"

urlpatterns = [
    path('timezone-time/<str:timezone>/', views.TimezoneTimeDetailAPIView.as_view()),
]

from django.urls import path

from . import views

app_name = "videochat"

urlpatterns = [
    path('test/', views.Test.as_view(), ),
]

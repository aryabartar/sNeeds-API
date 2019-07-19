from django.urls import path

from . import views

urlpatterns = [
    path('request/', views.SendRequest.as_view(), name='request'),
    path('verify/', views.verify, name='verify'),
]

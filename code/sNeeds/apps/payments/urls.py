from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    path('request/', views.SendRequest.as_view(), name='request'),
    path('verify/', views.Verify.as_view(), name='verify'),
    path('verify-test/<int:cartid>/', views.VerifyTest.as_view()),
]

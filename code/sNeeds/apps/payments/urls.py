from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    path('request/<int:cartid>', views.SendRequest.as_view(), name='request'),
    path('verify/', views.Verify.as_view(), name='verify'),
    path('verify-test/', views.VerifyTest.as_view(), name='verify-test'),
]

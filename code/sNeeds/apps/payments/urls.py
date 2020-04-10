from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    path('request/', views.SendRequest.as_view(), name='request'),
    path('verify/', views.Verify.as_view(), name='verify'),
    path('verify-test/<int:cartid>/', views.VerifyTest.as_view()),
    path('consultant-deposits/', views.ConsultantDepositInfoListAPIView.as_view(), name='consultant-deposit-list'),
    path('consultant-deposits/<str:consultant_deposit_info_id>/', views.ConsultantDepositInfoDetailAPIView.as_view(),
         name='consultant-deposit-detail'),
]

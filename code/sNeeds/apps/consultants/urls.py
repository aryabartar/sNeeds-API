from django.urls import path
from . import views

app_name = "consultant"

urlpatterns = [
    path('consultant-profiles/', views.ConsultantProfileList.as_view(), name="consultant-profile-list"),
    path('consultant-profiles/<str:slug>/', views.ConsultantProfileDetail.as_view(), name="consultant-profile-detail"),
]

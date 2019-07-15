from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('countries/', views.CountryList.as_view(), name="country-list"),
    path('countries/<str:slug>/', views.CountryDetail.as_view(), name="country-detail"),

    path('universities/', views.UniversityList.as_view(), name="university-list"),
    path('universities/<str:slug>/', views.UniversityDetail.as_view(), name="university-detail"),

    path('field-of-studies/', views.FieldOfStudyList.as_view(), name="field-of-study-list"),
    path('field-of-studies/<str:slug>/', views.FieldOfStudyDetail.as_view(), name="field-of-study-detail"),

    path('is-consultant/', views.CheckConsultantProfileView.as_view()),
    path('consultant-profiles/', views.ConsultantProfileList.as_view(), name="consultant-profile-list"),
    path('consultant-profiles/<str:slug>/', views.ConsultantProfileDetail.as_view(), name="consultant-profile-detail"),


]

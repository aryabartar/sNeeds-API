from django.urls import path

import sNeeds.apps.consultants.views
from . import views

app_name = "account"

urlpatterns = [
    path('countries/', views.CountryList.as_view(), name="country-list"),
    path('countries/<str:slug>/', views.CountryDetail.as_view(), name="country-detail"),

    path('universities/', views.UniversityList.as_view(), name="university-list"),
    path('universities/<str:slug>/', views.UniversityDetail.as_view(), name="university-detail"),

    path('field-of-studies/', views.FieldOfStudyList.as_view(), name="field-of-study-list"),
    path('field-of-studies/<str:slug>/', views.FieldOfStudyDetail.as_view(), name="field-of-study-detail"),

    path('consultant-profiles/', sNeeds.apps.consultants.views.ConsultantProfileList.as_view(),
         name="consultant-profile-list"),

    path('consultant-profiles/<str:slug>/', sNeeds.apps.consultants.views.ConsultantProfileDetail.as_view(),
         name="consultant-profile-detail"),

    path('user-detailed-info/', views.StudentDetailedInfoListCreateAPIView.as_view(),
         name='user-detailed-info-list'),

    path('user-detailed-info/<int:id>', views.StudentDetailedInfoRetrieveUpdateAPIView.as_view(),
         name='user-detailed-info-detail'),
    ]

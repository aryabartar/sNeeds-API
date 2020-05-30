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

    path('student-detailed-info/', views.StudentDetailedInfoListCreateAPIView.as_view(),
         name='student-detailed-info-list'),
    path('student-detailed-info/<int:id>/', views.StudentDetailedInfoRetrieveUpdateAPIView.as_view(),
         name='student-detailed-info-detail'),
    path('user-student-detailed-info/<int:user_id>/', views.UserStudentDetailedInfoRetrieveAPIView.as_view(),
         name='user-student-detailed-info-detail'),

    path('student-form-fields-choices/', views.StudentFormFieldsChoiceListAPIView.as_view(),
         name="student_form_fields_choice-list"),
    path('student-form-fields-choices/<int:id>/', views.StudentFormFieldsChoiceRetrieveAPIView.as_view(),
         name="student_form_fields_choice-detail"),

    path('student-form-semester-year-choices/', views.StudentFormApplySemesterYearListAPIView.as_view(),
         name="student_form_fields_choice-list"),
    path('student-form-semester-year-choices/<int:id>', views.StudentFormApplySemesterYearRetrieveAPIView.as_view(),
         name="student_form_fields_choice-detail"),
    ]

"""sNeeds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import  path
from . import views

urlpatterns = [
    path('countries/', views.CountryList.as_view(), name="country-list"),
    path('countries/<str:slug>', views.CountryDetail.as_view(), name="country-detail"),

    path('universities/', views.UniversityList.as_view(), name="university-list"),
    path('universities/<str:slug>', views.UniversityDetail.as_view(), name="university-detail"),

    path('field-of-studies/', views.FieldOfStudyList.as_view(), name="field-of-study-list"),
    path('field-of-studies/<str:slug>', views.FieldOfStudyDetail.as_view(), name="field-of-study-detail"),

    path('consultant-profiles/', views.ConsultantProfileList.as_view(), name="consultant-profile-list"),
    path('consultant-profiles/<str:slug>', views.ConsultantProfileDetail.as_view(), name="consultant-profile-detail"),
]

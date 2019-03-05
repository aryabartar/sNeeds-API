"""sneeds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from . import views
from rest_framework_jwt.views import refresh_jwt_token

app_name = "account"
urlpatterns = [

    path('my-account/', views.MyAccountDetail.as_view()),
    path('my-account/post-likes/', views.AccountLikedPosts.as_view()),
    path('my-account/booklet-downloads/', views.AccountDownloadBooklet.as_view()),

    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('jwt/login/', views.AuthView.as_view()),
    path('jwt/register/', views.RegisterView.as_view()),
    path('jwt/refresh/', refresh_jwt_token),
]

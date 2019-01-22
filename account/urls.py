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
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"
urlpatterns = [
    path('signup/success/', views.signup_success, name="signup_success"),
    path('signup/', views.signup, name="signup"),
    path('signup-new/', views.signup1, name="signup1"),
    path('logout/success/', views.logout_success, name="logout_success"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login_page.html'), name='login'),

    # TODO: Change _ with -
    path('my-account/', views.my_account, name="my_account"),
    path('cafe-profile-new/', views.cafe_profile, name="cafe_profile"),
    path('my-account/discount-archive/', views.all_cafe_archive, name='cafe_discount_archives'),
    path('delete/discount/', views.delete_user_discount, name='delete_discount'),
    path('delete/cafe-discount/', views.delete_cafe_discount, name='delete_cafe_discount'),
]

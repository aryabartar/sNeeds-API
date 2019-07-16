from django.urls import path

from rest_framework_jwt.views import refresh_jwt_token

from . import views
from sNeeds.apps.carts import views as cart_views

app_name = "auth"

urlpatterns = [
    path('jwt/token/', views.AuthView.as_view()),
    path('jwt/token/refresh/', refresh_jwt_token),

    path('accounts/', views.UserListView.as_view()),
    path('accounts/<int:id>/', views.UserDetailView.as_view()),
    path('accounts/<int:id>/cart/', cart_views.CartDetailView.as_view()),
]

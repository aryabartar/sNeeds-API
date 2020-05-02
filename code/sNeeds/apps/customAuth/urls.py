from django.urls import path, include

import sNeeds.apps.account.views
from rest_framework_simplejwt import views as jwt_views

from . import views

app_name = "auth"

urlpatterns = [
    # path('jwt/token/', views.AuthView.as_view()),
    # path('jwt/token/refresh/', refresh_jwt_token),
    path('jwt/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('accounts/', views.UserListView.as_view()),
    path('accounts/<int:id>/', views.UserDetailView.as_view()),

    path('my-account/', views.MyAccountInfoView.as_view()),
]

from django.urls import path, include

from rest_framework_jwt.views import refresh_jwt_token

from . import views

app_name = "auth"

urlpatterns = [
    path('jwt/token/', views.AuthView.as_view()),
    path('jwt/token/refresh/', refresh_jwt_token),

    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('accounts/', views.UserListView.as_view()),
    path('accounts/<int:id>/', views.UserDetailView.as_view()),

    path('my-account/', views.MyAccountInfoView.as_view()),
    path('user-detailed-info/', views.StudentDetailedInfoListCreateAPIView.as_view(), name='user-detailed-info-list'),
    path('user-detailed-info/<int:id>', views.StudentDetailedInfoRetrieveUpdateAPIView.as_view(),
         name='user-detailed-info-detail'),
]

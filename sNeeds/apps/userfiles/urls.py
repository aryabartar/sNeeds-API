from django.urls import path
from . import views

app_name = "userfiles"

urlpatterns = [
    path('user-files/', views.UserFileListView.as_view()),
    path('user-files/<int:id>/', views.UserFileDetailView.as_view(), name='user-file-detail'),
]

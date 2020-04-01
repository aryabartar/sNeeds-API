from django.urls import path
from . import views
app_name = "customForms"
urlpatterns = [
    path('bugs/', views.BugReportCreateAPIView.as_view(), name='bug-report-create'),
]

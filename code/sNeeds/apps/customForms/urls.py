from django.urls import path
from.views import BugReportCreateAPIView
app_name = "customForms"
urlpatterns = [
    path('bugs', BugReportCreateAPIView.as_view(), name='bug-report-create'),
]

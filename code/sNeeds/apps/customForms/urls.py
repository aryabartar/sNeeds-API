from django.urls import path
from.views import SendBug
app_name = "customForms"
urlpatterns = [
    path('bug', SendBug.as_view(), name='bug-create'),
]

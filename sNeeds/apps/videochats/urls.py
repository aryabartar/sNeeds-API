from django.urls import path

from . import views

app_name = "videochat"

urlpatterns = [
    path('rooms/', views.RoomListView.as_view()),

]

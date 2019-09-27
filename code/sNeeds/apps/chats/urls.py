from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path('chats/', views.ChatListAPIView.as_view(), name="chat-list"),
    path('chats/<int:id>', views.ChatDetailAPIView.as_view(), name="chat-detail"),
]

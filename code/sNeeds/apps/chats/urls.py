from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path('chats/', views.ChatListAPIView.as_view(), name="chat-list"),
    path('chats/<int:id>/', views.ChatDetailAPIView.as_view(), name="chat-detail"),
    path('text-messages/', views.TextMessageListAPIView.as_view(), name="text-message-list"),
    path('text-messages/<int:id>/', views.TextMessageDetailAPIView.as_view(), name="text-message-detail"),
]

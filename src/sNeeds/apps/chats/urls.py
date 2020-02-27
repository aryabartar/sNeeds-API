from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path('chats/', views.ChatListAPIView.as_view(), name="chat-list"),
    path('chats/<int:id>/', views.ChatDetailAPIView.as_view(), name="chat-detail"),
    path('messages/', views.MessageListAPIView.as_view(), name="message-list"),
    path('messages/<int:id>/', views.MessageDetailAPIView.as_view(), name="message-detail"),
    path('admin/', views.admin_chat_peek, name="admin-chat-list"),
    path('admin/<int:id>/', views.admin_chat_messages_peek, name="admin-chat-detail"),
]

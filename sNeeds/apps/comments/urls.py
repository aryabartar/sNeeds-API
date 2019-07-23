from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path('comments/', views.CommentListView.as_view(), name="comment-list"),
    path('comments/<int:id>/', views.CommentDetailView.as_view(), name="comment-detail"),
    path('admin-comments/', views.AdminCommentListView.as_view(), name="admin-comment-list"),
]

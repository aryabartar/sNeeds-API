from django.contrib import admin
from .models import Topic, Post, UserComment
from .forms import PostForm

admin.site.register(Topic)


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'updated', 'timestamp']
    form = PostForm


class UserCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'user']

    class Meta:
        model = UserComment


admin.site.register(Post, PostAdmin)
admin.site.register(UserComment, UserCommentAdmin)

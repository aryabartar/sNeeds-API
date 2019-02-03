from django.contrib import admin
from .models import Topic, Post
from .forms import PostForm

admin.site.register(Topic)


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'updated', 'timestamp']
    form = PostForm


admin.site.register(Post, PostAdmin)

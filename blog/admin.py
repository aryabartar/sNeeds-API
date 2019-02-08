from django.contrib import admin
from .models import Topic, Post, UserComment, AdminComment

admin.site.register(Topic)


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'slug', 'updated', 'timestamp']

    class Meta:
        model = Post


class UserCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'post', 'user']

    class Meta:
        model = UserComment


admin.site.register(Post, PostAdmin)
admin.site.register(UserComment, UserCommentAdmin)
admin.site.register(AdminComment)

from django.contrib import admin
from .models import Topic, Post, BookletTopic, Booklet, BookletField, UserUploadedBooklet, BookletProblemReport

# Register your models here.
admin.site.register(Booklet)
admin.site.register(BookletField)
admin.site.register(BookletTopic)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(UserUploadedBooklet)
admin.site.register(BookletProblemReport)

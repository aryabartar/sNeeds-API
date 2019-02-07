from django.db import models
from django.conf import settings
from django.urls import reverse


class Topic(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    slug = models.SlugField(null=True, unique=True)

    def get_absolute_url(self):
        return reverse('blog:topic', kwargs={"topic_slug": self.slug})

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    topic = models.ForeignKey(Topic, null=True, related_name="posts", on_delete=models.SET_NULL)
    content = models.TextField(null=False, blank=False)
    tags = models.CharField(max_length=200, null=True, blank=True, help_text="Sample form : آریا، آمریکا، اپلای")
    slug = models.SlugField(null=False, default="", unique=True)

    updated = models.DateTimeField(auto_now=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={"topic_slug": self.topic.slug, "post_slug": self.slug})

    def __str__(self):
        return "{}".format(self.title)


class UserComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    content = models.TextField(null=False, blank=False, max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return "{}".format(self.content)


class AdminComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    content = models.TextField(null=False, blank=False, max_length=400)
    user_comment = models.OneToOneField(UserComment, on_delete=models.CASCADE, related_name="admin_comment")

    def __str__(self):
        return "{}".format(self.content)


class HelloModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.title) + str(self.content)

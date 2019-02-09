from django.db import models
from django.conf import settings
from django.urls import reverse
from django_jalali.db import models as jmodels


class Topic(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    slug = models.SlugField(null=True, unique=True)

    def get_absolute_url(self):
        return reverse('blog:topic', kwargs={"topic_slug": self.slug})

    def __str__(self):
        return self.title


def upload_post_image(instance, filename):
    return "status/{slug}/{filename}".format(slug=instance.slug, filename=filename)


class Post(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    topic = models.ForeignKey(Topic, null=True, related_name="posts", on_delete=models.SET_NULL)
    post_main_image = models.ImageField(upload_to=upload_post_image, null=False, default="")
    POST_TYPE = (
        ('Q&A', 'Question and Answer'),
        ('interview', 'Interview'),
    )
    post_type = models.CharField(choices=POST_TYPE, default='Q&A', null=False, blank=False, max_length=50)
    short_description = models.TextField(null=True, blank=True)
    aparat_link = models.URLField(null=True,
                                  blank=True,
                                  help_text="Don't fill this if this post has no "
                                            "video.\nSapmle: https://www.aparat.com/v/4Y7PV "
                                  )
    youtube_link = models.URLField(null=True,
                                   blank=True,
                                   help_text="Don't fill this if this post has no "
                                             "video.\nSample: https://www.youtube.com/watch?v=h1QkGnI4P6g "
                                   )
    tags = models.CharField(max_length=200, null=True, blank=True, help_text="Sample form : آریا، آمریکا، اپلای")
    slug = models.SlugField(null=False, default="", unique=True)

    updated = models.DateTimeField(auto_now=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    timestamp_jalali = jmodels.jDateField(auto_now_add=True, null=True)

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={"topic_slug": self.topic.slug, "post_slug": self.slug})

    def __str__(self):
        return "{}".format(self.title)


class PostQuestionAnswer(models.Model):
    content = models.TextField()


class PostQuestion(models.Model):
    content = models.TextField()
    answer = models.OneToOneField(PostQuestionAnswer , on_delete=models.CASCADE)


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

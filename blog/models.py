from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return self.title


class PostQuerySet(models.QuerySet):
    pass


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)


class Post(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    content = models.TextField(null=False, blank=False)
    topic = models.ForeignKey(Topic, null=True, related_name="posts", on_delete=models.SET_NULL)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        verbose_name = "Post title"
        verbose_name_plural = "Post titles"
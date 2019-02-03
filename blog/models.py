from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    slug = models.SlugField(null=True, unique=True)


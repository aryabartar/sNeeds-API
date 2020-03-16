from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


def get_bug_image_path(instance, filename):
    return "images/bugs/{}/image/{}".format(instance.email, filename)


class BugReport(models.Model):
    picture = models.ImageField(blank=True, upload_to=get_bug_image_path)
    comment = models.CharField(max_length=1024)
    email = models.EmailField(blank=True, max_length=128)

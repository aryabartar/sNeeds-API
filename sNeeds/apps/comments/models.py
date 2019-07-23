from django.db import models
from django.contrib.auth import get_user_model

from sNeeds.apps.account.models import ConsultantProfile

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "User : {} | Consultant : {}".format(str(self.user), str(self.consultant))


class AdminComment(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name="admin_reply")
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Comment {} Reply".format(self.comment)

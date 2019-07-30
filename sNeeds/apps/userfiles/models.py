from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

USER_FILE_CHOICES = (
    ('resume', 'Resume'),
)


def get_file_upload_path(sub_dir):
    return "file/account/" + sub_dir


class UserFileModelManager(models.Manager):
    def get_consultant_accessed_files(self, consultant_profile):
        from sNeeds.apps.store.models import SoldTimeSlotSale

        sold_to_list = SoldTimeSlotSale.objects.filter(
            consultant=consultant_profile,
        ).values_list('sold_to', flat=True)

        qs = UserFile.objects.filter(user__in=sold_to_list)
        return qs


class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_file_upload_path("user_upload_file"))
    type = models.CharField(max_length=256, choices=USER_FILE_CHOICES)

    objects = UserFileModelManager()

    class Meta:
        unique_together = ('user', 'type')

    def __str__(self):
        return self.user.__str__()

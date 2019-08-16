from django.db import models
from sNeeds.apps.customAuth.models import CustomUser
from os.path import isfile
from os import remove
from django.dispatch import receiver


def path_for_uploading_file(instance, filename):
    return "tweet/{email}/{filename}".format(email=instance.sender.email, filename=filename)


class TweetModel(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    date_created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False, blank=False, null=False)
    edited = models.BooleanField(default=False)
    file = models.FileField(upload_to=path_for_uploading_file, null=True, blank=True)
    text = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return self.text

@receiver(models.signals.post_delete, sender=TweetModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `TweetModel` object is deleted.
    """
    if instance.file:
        if isfile(instance.file.path):
            remove(instance.file.path)

@receiver(models.signals.pre_save, sender=TweetModel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = TweetModel.objects.get(pk=instance.pk).file
    except TweetModel.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if isfile(old_file.path):
            remove(old_file.path)

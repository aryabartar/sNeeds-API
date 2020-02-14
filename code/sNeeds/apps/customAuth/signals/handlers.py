from django.db.models.signals import post_save

from sNeeds.apps.customAuth.models import ConsultantProfile


def post_save_consultant_profile(sender, instance, created, *args, **kwargs):
    print("Hello")


post_save.connect(post_save_consultant_profile, sender=ConsultantProfile)

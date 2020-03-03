from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from sNeeds.apps.consultants.models import ConsultantProfile

User = get_user_model()


def post_save_consultant_profile(sender, instance, created, *args, **kwargs):
    users_qs = User.objects.all()
    for user in users_qs:
        try:
            ConsultantProfile.objects.get(user=user)
            user.set_user_type_consultant()
        except ConsultantProfile.DoesNotExist:
            user.set_user_type_student()


post_save.connect(post_save_consultant_profile, sender=ConsultantProfile)

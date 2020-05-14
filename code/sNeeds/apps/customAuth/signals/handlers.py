from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.customAuth.tasks import send_reset_password_email
from sNeeds.settings.config.variables import FRONTEND_URL

User = get_user_model()


def post_save_consultant_profile(sender, instance, created, *args, **kwargs):
    users_qs = User.objects.all()

    for user in users_qs:
        user.update_user_type()
        user.save()


post_save.connect(post_save_consultant_profile, sender=ConsultantProfile)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.first_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            reverse('auth:password_reset:reset-password-request'),
            reset_password_token.key
        ),
        'token': reset_password_token.key,
    }
    reset_link = FRONTEND_URL + "auth/forget?token={}".format(context['token'])

    send_reset_password_email.delay(
        context['email'],
        context['current_user'].get_full_name(),
        reset_link,
    )

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from .tasks import send_reset_password_email


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.first_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(reverse('auth:password_reset:reset-password-request'),
                                                   reset_password_token.key),
        'token': reset_password_token.key,
    }
    reset_link = "http://193.176.241.131:8080/account/password-reset/?token={}".format(context['token'])

    send_reset_password_email.delay(
        context['email'],
        context['current_user'].first_name,
        reset_link,
    )

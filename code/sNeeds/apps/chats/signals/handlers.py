from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model

from sNeeds.apps.chats.models import Chat, TextMessage
from sNeeds.apps.consultants.models import ConsultantProfile

User = get_user_model()


def post_save_user(sender, instance, created, *args, **kwargs):
    if created:
        admin_consultant_user = User.objects.get_admin_consultant_or_none()
        if admin_consultant_user is not None and ConsultantProfile.objects.filter(user=admin_consultant_user).exists():
            chat = Chat.objects.create(
                user=instance,
                consultant=ConsultantProfile.objects.get(user=admin_consultant_user)
            )
            TextMessage.objects.create(
                chat=chat,
                sender=admin_consultant_user,
                text_message="\
                    سلام به جمع ۱۲۰۰ کاربر اسنیدز خوش اومدی!\r\nاینجا پیام‌های مهم از طرف اسنیدز برات فرستاده می‌شه. همین طور تو قسمت چت می‌تونی با مشاوری که باهاش تایم مشاوره رزرو کردی در ارتباط باشی!\r\nهر سوالی هم در مورد استفاده از سایت و خدماتمون داری می‌تونی همینجا بپرسی و ما خیلی سریع بهت جواب می‌دیم.\
                "
            )

            TextMessage.objects.create(
                chat=chat,
                sender=admin_consultant_user,
                text_message=" \
                    شماره تماس ما: 09221496645\r\nایمیل: info@sneeds.ir\r\nپشتیبانی تلگرام: ‌sneeds_admin@\
                  "
            )


post_save.connect(post_save_user, sender=User)

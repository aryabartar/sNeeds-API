import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'sneeds.settings.production'

django.setup()

from blog.models import Topic, Post, UserComment, AdminComment
from booklet.models import BookletField, BookletTopic, Booklet
from faker import Faker
from random import randint

fake = Faker()


def populate_topic():
    for i in range(0, 10):
        new_topic = Topic(title="کشور تست {} ".format(str(i + 1)), slug=fake.slug())
        new_topic.save()


def populate_post():
    all_topics = Topic.objects.all()
    all_topics_number = len(all_topics)

    for i in range(1, 201):
        new_post = Post(
            title="پست تست {}".format(str(i)),
            topic=all_topics[randint(0, all_topics_number - 1)],
            post_main_image=Post.objects.first().post_main_image,
            content="لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. "
                    "چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است و برای شرایط فعلی تکنولوژی "
                    "مورد نیاز و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد. کتابهای زیادی در شصت و سه "
                    "درصد گذشته، حال و آینده شناخت فراوان جامعه و متخصصان را می طلبد تا با نرم افزارها شناخت بیشتری "
                    "را برای طراحان رایانه ای علی الخصوص طراحان خلاقی و فرهنگ پیشرو در زبان فارسی ایجاد کرد. در این "
                    "صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها و شرایط سخت تایپ به پایان رسد "
                    "وزمان مورد نیاز شامل حروفچینی دستاوردهای اصلی و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی "
                    "اساسا مورد استفاده قرار گیرد.",
            tags="ایران، اپلای، توسعه، رشته عمران، چگونه اپلای کنیم، آیا اپلای به آمریکا خوب است",
            slug=fake.slug(),
            aparat_link="https://www.aparat.com/v/4Y7PV",
            youtube_link="https://www.youtube.com/watch?v=h1QkGnI4P6g",

        )
        new_post.save()


def populate_comments():
    all_posts = Post.objects.all()
    all_posts_number = len(all_posts)
    first_comment = UserComment.objects.first()

    for i in range(1, 300):
        content = "این یه کامنت تسته. این کامنت خیلی خوشگله و سایت خوشگل‌تر. خسته نباشی رفیق ایام به کام :))"
        user = first_comment.user
        post = all_posts[randint(0, all_posts_number - 1)]
        obj = UserComment(user=user, post=post, content=content)
        obj.save()


def populate_admin_answer():
    all_comments = UserComment.objects.all()
    all_comments_number = len(all_comments)

    for i in range(0, all_comments_number // 2):
        try:
            content = "من ادمینم و مثلا بهت یه جواب دادم. ایول که اومدی کامنت گذاشتی. خیلی حال دادی"
            comment = all_comments[randint(0, all_comments_number - 1)]
            obj = AdminComment(content=content, user_comment=comment)
            obj.save()
        except:
            pass


def populate_short_description_field():
    all_posts = Post.objects.all()
    for post in all_posts:
        post.short_description = "فیلم Widows به کارگردانی استیو مک‌کویین بعد از «ماموریت غیرممکن: فال‌اوت»، بهترین بلاک‌باسترِ اولد-اسکول سال ۲۰۱۸ است. همراه نقد آریا برتر باشید."
        post.save()


def booklet_field():
    for i in range(1, 10):
        title = "رشته تست {}".format(str(i))
        slug = "test-field-{}".format(str(i))
        new_field = BookletField(title=title, slug=slug)
        new_field.save()


def booklet_topic():
    all_fields = BookletField.objects.all()
    all_fields_number = len(all_fields)
    for i in range(1, 80):
        title = "درس تست {}".format(str(i))
        slug = "test-topic-{}".format(str(i))
        field = all_fields[randint(0, all_fields_number - 1)]
        new_topic = BookletTopic(title=title, slug=slug, field=field)
        new_topic.save()


def booklet():
    all_topics = BookletTopic.objects.all()
    all_topics_number = len(all_topics)
    for i in range(1, 300):
        title = "جزوه تست {}".format(i)
        information = "معماری کامپیوتر دانش طراحی مفهومی و شناخت اجزای رایانه است. عنوان یکی از گرایش‌های کامپیوتر است. در این گرایش با اجزای داخلی کامپیوتر که مراحل انجام یک دستور را بر عهده دارند و چگونگی کار آنها آشنا میشویم. در این گرایش واحد کنترل مرکزی و حافظه به عنوان دو بخش اصلی کامپیوتر معرفی میشوند و در ادامه به بررسی ارتباط آنها و ساختار درونی آنها میپردازند. برای درک موضوعات مطرح شده در این گرایش آشنائی با مبحث مدارهای منطقی لازم و ضروری است."
        topic = all_topics[randint(0, all_topics_number - 1)]
        teacher = "آریا برتر کبیر"
        number_of_pages = randint(20, 140)
        format = "PDF"
        if randint(0, 3) == 1:
            format = "ZIP"
        language = 'farsi'
        if randint(0, 3) == 1:
            language = "english"
        slug = fake.slug()
        number_of_likes = randint(0, 4)
        booklet_content = Booklet.objects.first().booklet_content
        booklet_image = Booklet.objects.first().booklet_image

        new_booklet = Booklet(
            title=title,
            information=information,
            topic=topic,
            teacher=teacher,
            number_of_pages=number_of_pages,
            format=format,
            language=language,
            slug=slug,
            number_of_likes=number_of_likes,
            booklet_content=booklet_content,
            booklet_image=booklet_image,
        )
        new_booklet.save()


# populate_topic()
# populate_post()
# populate_comments()
# populate_admin_answer()

# booklet_field()
# booklet_topic()
booklet()

import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'sneeds.settings.production'

django.setup()

from blog.models import Topic, Post
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


populate_topic()
populate_post()

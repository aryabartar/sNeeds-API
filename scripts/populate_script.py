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
        new_topic = Topic(title="Test title {}".format(str(i)), slug=fake.slug())
        new_topic.save()


def populate_post():
    all_topics = Topic.objects.all()
    all_topics_number = len(all_topics)

    for i in range(0, 200):
        new_post = Post(
            title="test title {}".format(str(i)),
            topic=all_topics[randint(0, all_topics_number-2)],
            content=fake.text(),
            tags="not generated",
            slug=fake.slug()
        )
        new_post.save()


# populate_topic()
populate_post()
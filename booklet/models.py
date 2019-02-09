from django.db import models

from django.urls import reverse
from django.utils import timezone


class BookletField(models.Model):
    """
    For example Civil Eng, Computer Eng, ...
    """
    title = models.CharField(max_length=120, blank=False, null=False, unique=True)
    slug = models.SlugField(null=True, help_text="Lower case")

    def get_absolute_url(self):
        return reverse('booklet:get_field', kwargs={"field_slug": self.slug})

    def __str__(self):
        return self.title


class BookletTopic(models.Model):
    """
    For example AP, DS, Environment, ...
    """
    field = models.ForeignKey(BookletField,
                              on_delete=models.CASCADE,
                              related_name='topics',
                              blank=False,
                              null=False)
    title = models.CharField(max_length=120,
                             blank=False,
                             null=False,
                             help_text="Sample: برنامه‌نویسی پیشرفته"
                             )
    slug = models.SlugField(null=False, help_text="Lower case |Sample: advanced-programming")

    def get_absolute_url(self):
        return reverse('booklet:get_topic', kwargs={'field_slug': self.field.slug, 'topic_slug': self.slug})

    def __str__(self):
        temp_str = self.title + " | " + self.field.title
        return temp_str


class Booklet(models.Model):
    title = models.CharField(max_length=200, blank=False)
    information = models.TextField(max_length=10000, null=True)
    topic = models.ForeignKey(BookletTopic, on_delete=models.CASCADE,
                              related_name='booklets',
                              null=False,
                              blank=False
                              )

    teacher = models.CharField(max_length=200, default=None)
    slug = models.SlugField(unique=True, null=False, blank=False)

    number_of_views = models.IntegerField(default=0,
                                          help_text="لطفا مقدار را عوض نکنید ( به جز در مواقع نیاز شدید و باگ)",
                                          verbose_name="تعداد بازدید")

    booklet_content = models.FileField(upload_to="website/booklet_content", blank=False)
    booklet_image = models.ImageField(upload_to="website/booklet_images", blank=False)

    # def get_absolute_url(self):
    #     """Returns the url to access a detail record for this book."""
    #     return reverse('website:booklets', args=[str(self.slug)])

    def __str__(self):
        return self.title

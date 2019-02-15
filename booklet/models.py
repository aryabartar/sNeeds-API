from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify


def get_automated_slug(str):
    "I write this function because slugify is not working for persian characters!"
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str


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


class Tag(models.Model):
    title = models.CharField(max_length=40, null=False, blank=False)
    slug = models.SlugField(max_length=2000, unique=True,
                            help_text="If you are adding this tag for first time, leave this field blank."
                                      "Only change this field if there is a mistake or for other purposes ...")

    def save(self, *args, **kwargs):
        self.slug = get_automated_slug(self.title)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Booklet(models.Model):
    title = models.CharField(max_length=200, blank=False)
    information = models.TextField(max_length=10000, null=True)
    topic = models.ForeignKey(BookletTopic, on_delete=models.CASCADE,
                              related_name='booklets',
                              null=False,
                              blank=False
                              )

    teacher = models.CharField(max_length=200, default=None)
    number_of_pages = models.IntegerField(default=0, null=False, blank=False, help_text="حتما دقیق نوشته شود")
    format = models.CharField(max_length=40, default="PDF", null=False, blank=False)
    year = models.IntegerField(help_text="In 1397 format.", null=True, blank=True)
    writer = models.CharField(max_length=120, null=True, blank=True)

    BOOKLET_LANGUAGE = (
        ('farsi', "فارسی"),
        ('english', "انگلیسی"),
    )

    language = models.CharField(choices=BOOKLET_LANGUAGE, default='farsi', null=False, blank=False, max_length=50)
    slug = models.SlugField(unique=True, null=False, blank=False)
    tags_str = models.CharField(max_length=2000, blank=True, null=True,
                                help_text="به این صورت وارد کنید : <br/>"
                                          "جزوه ریاضی|بهترین جزوه عالم|جزوه بخون حالشو ببر")
    tags = models.ManyToManyField(Tag, null=True, blank=True,
                                  help_text="Don't change this if you are creating new booklet. Only change this if "
                                            "it is necessary.")
    number_of_views = models.IntegerField(default=0,
                                          help_text="لطفا مقدار را عوض نکنید ( به جز در مواقع نیاز شدید و باگ)",
                                          verbose_name="تعداد بازدید")
    number_of_likes = models.IntegerField(default=0)
    booklet_content = models.FileField(upload_to="website/booklet_content", blank=False)
    booklet_image = models.ImageField(upload_to="website/booklet_images", blank=False)

    def get_absolute_url(self):
        return reverse('booklet:get_booklet', kwargs={'booklet_slug': self.slug,
                                                      'field_slug': self.topic.field.slug,
                                                      'topic_slug': self.topic.slug})

    def get_tags_array(self):
        if self.tags_str is not None:
            return self.tags_str.split("|")
        return []

    def save(self, *args, **kwargs):
        tags = self.get_tags_array()
        for tag in tags:
            qs = Tag.objects.filter(slug__exact=get_automated_slug(tag))
            if len(qs) == 0:
                new_tag = Tag(title=tag)
                new_tag.save()
            else:
                qs[0].save()
            self.tags.add(Tag.objects.filter(slug__exact=get_automated_slug(tag))[0])
        super(Booklet, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

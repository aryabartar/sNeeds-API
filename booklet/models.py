from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
import django.contrib.auth.password_validation as validators


User = get_user_model()


class BookletField(models.Model):
    """
    For example Civil Eng, Computer Eng, ...
    """
    title = models.CharField(max_length=120, blank=False, null=False, unique=True)
    slug = models.SlugField(null=True, help_text="Lower case", unique=True)

    def get_absolute_url(self):
        return reverse('booklet:fields_detail', kwargs={"field_slug": self.slug})

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
    information = models.TextField(max_length=10000, null=True , blank=True , help_text="Can be empty")
    slug = models.SlugField(null=False,
                            unique=True,
                            help_text="Lower case |Sample: advanced-programming")

    def get_absolute_url(self):
        return reverse('booklet:topics_detail', kwargs={'topic_slug': self.slug})

    def __str__(self):
        temp_str = self.title + " | " + self.field.title
        return temp_str


class Tag(models.Model):
    title = models.CharField(max_length=40, null=False, blank=False)
    slug = models.SlugField(max_length=2000, unique=True,
                            help_text="If you are adding this tag for first time, leave this field blank."
                                      "Only change this field if there is a mistake or for other purposes ...")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('booklet:tags_detail', kwargs={"tag_slug": self.slug})


def upload_booklet_image(instance, filename):
    return "booklet/booklet_image/{slug}/{filename}".format(slug=instance.slug, filename=filename)


class Booklet(models.Model):
    title = models.CharField(max_length=200, blank=False)
    topic = models.ForeignKey(BookletTopic, on_delete=models.CASCADE,
                              related_name='booklets',
                              null=False,
                              blank=False
                              )
    slug = models.SlugField(unique=True, null=False, blank=False)

    teacher = models.CharField(max_length=200, null=True, blank=True)
    number_of_pages = models.IntegerField(default=0, null=True, blank=True, help_text="حتما دقیق نوشته شود")
    format = models.CharField(max_length=40, default="PDF", null=False, blank=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name="booklets",
                                  help_text="Don't change this if you are creating new booklet. Only change this if "
                                            "it is necessary.")

    BOOKLET_LANGUAGE = (
        ('farsi', "فارسی"),
        ('english', "انگلیسی"),
    )

    language = models.CharField(choices=BOOKLET_LANGUAGE, default='farsi', null=False, blank=False, max_length=50)
    year = models.IntegerField(help_text="In 1397 format.", null=True, blank=True)
    writer = models.CharField(max_length=120, null=True, blank=True)

    number_of_likes = models.IntegerField(default=0)

    booklet_image = models.ImageField(upload_to=upload_booklet_image, null=True)
    # booklet_image = models.ImageField( null=True)
    booklet_content = models.URLField()

    def get_absolute_url(self):
        return reverse('booklet:booklets_detail', kwargs={'booklet_slug': self.slug})

    def __str__(self):
        return self.title


class BookletDownload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booklet_downloads")
    booklet = models.ForeignKey(Booklet, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "booklet"),)

    def __str__(self):
        return str(self.booklet)

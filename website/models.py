from django.db import models
from django.utils import timezone


class Topic(models.Model):
    subject = models.CharField(max_length=120)
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='children' , on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __init__(self):
        super
        slug = models.SlugField(unique=True , default=self.pk)

    @models.permalink
    def get_absolute_url(self):
        return 'website:categories', (self.slug,)

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.subject]                  # post.  use __unicode__ in place of
                                                 # __str__ if you are using python 2
        k = self.parent

        while k is not None:
            full_path.append(k.subject)
            k = k.parent

        return ' -> '.join(full_path[::-1])



class BookletTopic(models.Model):
    subject = models.CharField(max_length=120)


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    post_image = models.ImageField(upload_to="website/post_images", blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Booklet(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,null = True)
    title = models.CharField(max_length=200 , blank=False)
    # Booklet writer name
    owner = models.CharField(max_length=200, blank=True, default="ناشناس")
    topic = models.ForeignKey(BookletTopic, on_delete=models.CASCADE, related_name='booklets' , blank=False)
    text = models.TextField()
    booklet_content = models.FileField(upload_to="website/booklet_content", blank=False)
    booklet_image = models.ImageField(upload_to="website/booklet_images", blank=False)

    def __str__(self):
        return self.title

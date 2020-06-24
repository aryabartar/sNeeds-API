from django.core.exceptions import ValidationError
from django.db import models, transaction
from sNeeds.apps.store.models import Product, SoldProduct, ProductQuerySet, SoldProductQuerySet
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


def get_lecturer_picture_path(instance, filename):
    return "basicProducts/lecturers/{}/image/{}".format(instance.id, filename)


def get_class_webinar_image_path(instance, filename):
    return "basicProducts/class_webinar/{}/image/{}".format(instance.id, filename)


def get_class_webinar_background_image_path(instance, filename):
    return "basicProducts/class_webinar/{}/image/{}".format(instance.id, filename)


# class BasicProductManager(models.QuerySet):
#     @transaction.atomic
#     def add_basic_product_sold(self, sold_to):
#         qs = self.all()
#
#         sold_basic_product_list = []
#         for obj in qs:
#             try:
#                 class_product = obj.classproduct
#                 sold_basic_product_list.append(
#                     SoldClassProduct.objects.create(
#                         basic_product=obj,
#                         sold_to=sold_to,
#                         price=obj.price,
#                     )
#                 )
#             except ClassProduct.DoesNotExist:
#                 pass
#
#             try:
#                 webinar_product = obj.webinarproduct
#                 sold_basic_product_list.append(
#                     SoldWebinarProduct.objects.create(
#                         basic_product=obj,
#                         sold_to=sold_to,
#                         price=obj.price,
#                     )
#                 )
#             except WebinarProduct.DoesNotExist:
#                 pass
#
#         sold_basic_product_qs = SoldBasicProduct.objects.filter(id__in=[obj.id for obj in sold_basic_product_list])
#
#         return sold_basic_product_qs


class ClassProductManager(models.QuerySet):
    @transaction.atomic
    def add_class_product_sold(self, sold_to):
        qs = self.all()

        sold_class_product_list = []
        for obj in qs:
            try:
                class_product = obj.classproduct
                sold_class_product_list.append(
                    SoldClassProduct.objects.create(
                        class_product=obj,
                        sold_to=sold_to,
                        price=obj.price,
                    )
                )
            except ClassProduct.DoesNotExist:
                pass

        sold_class_product_qs = SoldBasicProduct.objects.filter(id__in=[obj.id for obj in sold_class_product_list])

        return sold_class_product_qs


class WebinarProductManager(models.QuerySet):
    @transaction.atomic
    def add_webinar_product_sold(self, sold_to):
        qs = self.all()

        sold_webinar_product_list = []
        for obj in qs:
            try:
                webinar_product = obj.webinarproduct
                sold_webinar_product_list.append(
                    SoldWebinarProduct.objects.create(
                        class_product=obj,
                        sold_to=sold_to,
                        price=obj.price,
                    )
                )
            except WebinarProduct.DoesNotExist:
                pass

        sold_webinar_product_qs = SoldBasicProduct.objects.filter(id__in=[obj.id for obj in sold_webinar_product_list])

        return sold_webinar_product_qs


class BasicProduct(Product):
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    # objects = BasicProductManager.as_manager()

    def __str__(self):
        return self.slug


class SoldBasicProduct(SoldProduct):
    objects = SoldProductQuerySet.as_manager()


class HoldingDateTime(models.Model):
    date_time = models.DateTimeField()


class Lecturer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    picture = models.ImageField(upload_to=get_lecturer_picture_path)
    title = models.CharField(max_length=256)
    header = models.TextField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class QuestionAnswer(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question[:64]


class ClassWebinar(BasicProduct):
    image = models.ImageField(upload_to=get_class_webinar_image_path, blank=True, null=True)
    background_image = models.ImageField(upload_to=get_class_webinar_background_image_path, blank=True, null=True)
    descriptions = models.TextField(blank=True, null=True)
    headlines = models.TextField(blank=True, null=True)
    audiences = models.TextField(blank=True, null=True)
    lecturers = models.TextField(blank=True, null=True)
    lecturers_short = models.ManyToManyField(Lecturer, related_name="%(app_label)s_%(class)s")
    holding_date_times = models.ManyToManyField(HoldingDateTime, related_name="%(app_label)s_%(class)s")
    question_answers = models.ManyToManyField(QuestionAnswer, related_name="%(app_label)s_%(class)s")

    is_free = models.BooleanField(default=False)

    is_held = models.BooleanField(default=False)

    is_early = models.BooleanField(default=False)
    early_price = models.PositiveIntegerField(blank=True, null=True)
    regular_price = models.PositiveIntegerField(blank=True, null=True)

    video_is_discounted = models.BooleanField(default=False)
    video_regular_price = models.PositiveIntegerField(blank=True, null=True)
    video_discounted_price = models.PositiveIntegerField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " (" + str(self.id) + ")"

    def save(self, *args, **kwargs):
        self.full_clean()
        super(ClassWebinar, self).save(*args, **kwargs)

    def clean(self):
        price = None
        if self.is_free:
            price = 0

        elif self.is_held:
            if self.video_is_discounted:
                # if self.video_discounted_price is None:
                #     raise ValidationError(_("Due to information some credential not provided:video_discounted_price"))
                price = self.video_discounted_price

            else:
                # if self.video_regular_price is None:
                #     raise ValidationError(_("Due to information some credentials not provided: video_regular_price"))
                price = self.video_regular_price

        else:
            if self.is_early:
                # if self.early_price is None:
                #     raise ValidationError(_("Due to information some credentials not provided: early_price"))
                price = self.early_price
            else:
                # if self.regular_price is None:
                #     raise ValidationError(_("Due to information some credentials not provided: regular_price"))
                price = self.regular_price

        # if price is None:
        #     raise ValidationError(_("Due to information some credentials not provided: check is_free, is_held, "
        #                             "is_early, video_is_discounted "))

        self.price = price


class ClassProduct(ClassWebinar):
    type = models.CharField(max_length=10, default="class")
    objects = ClassProductManager.as_manager()


class WebinarProduct(ClassWebinar):
    type = models.CharField(max_length=10, default="webinar")
    objects = WebinarProductManager.as_manager()


class SoldClassWebinar(SoldBasicProduct):
    pass


class SoldClassProduct(SoldClassWebinar):
    class_product = models.ForeignKey(ClassProduct, on_delete=models.PROTECT, null=True)


class SoldWebinarProduct(SoldClassWebinar):
    webinar_product = models.ForeignKey(WebinarProduct, on_delete=models.PROTECT, null=True)


class DownloadLink(models.Model):
    product = models.ForeignKey(ClassWebinar, on_delete=models.CASCADE, related_name='downlaodlink')
    url = models.URLField()


class RoomLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(null=True, blank=True)


class WebinarRoomLink(RoomLink):
    product = models.ForeignKey(WebinarProduct, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s")

    # class Meta:
    #     unique_together = ['product', 'user']


class ClassRoomLink(RoomLink):
    product = models.ForeignKey(ClassProduct, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s")
    #
    # class Meta:
    #     unique_together = ['product', 'user']

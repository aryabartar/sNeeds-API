from django.db import models, transaction
from sNeeds.apps.store.models import Product, SoldProduct, ProductQuerySet, SoldProductQuerySet


def get_lecturer_picture_path(instance, filename):
    return "basicProducts/lecturers/{}/image/{}".format(instance.id, filename)


def get_class_webinar_image_path(instance, filename):
    return "basicProducts/class_webinar/{}/image/{}".format(instance.id, filename)


def get_class_webinar_background_image_path(instance, filename):
    return "basicProducts/class_webinar/{}/image/{}".format(instance.id, filename)


class BasicProductManager(models.QuerySet):
    @transaction.atomic
    def add_basic_product_sold(self, sold_to):
        qs = self.all()

        sold_basic_product_list = []
        for obj in qs:
            try:
                class_product = obj.classproduct
                sold_basic_product_list.append(
                    SoldClassProduct.objects.create(
                        basic_product=obj,
                        sold_to=sold_to,
                        price=obj.price,
                    )
                )
            except ClassProduct.DoesNotExist:
                pass

            try:
                webinar_product = obj.webinarproduct
                sold_basic_product_list.append(
                    SoldWebinarProduct.objects.create(
                        basic_product=obj,
                        sold_to=sold_to,
                        price=obj.price,
                    )
                )
            except ClassProduct.DoesNotExist:
                pass

        sold_basic_product_qs = SoldBasicProduct.objects.filter(id__in=[obj.id for obj in sold_basic_product_list])

        return sold_basic_product_qs


class BasicProduct(Product):
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    objects = BasicProductManager.as_manager()

    def __str__(self):
        return self.slug


class SoldBasicProduct(SoldProduct):
    basic_product = models.ForeignKey(BasicProduct, on_delete=models.PROTECT)

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


class ClassWebinarPrice(models.Model):
    early_price = models.PositiveIntegerField(blank=True)
    regular_price = models.PositiveIntegerField(blank=True)


class ClassWebinar(BasicProduct):
    image = models.ImageField(upload_to=get_class_webinar_image_path)
    background_image = models.ImageField(upload_to=get_class_webinar_background_image_path)
    descriptions = models.TextField()
    headlines = models.TextField()
    audiences = models.TextField()
    lecturers = models.TextField()
    lecturers_short = models.ManyToManyField(Lecturer)
    holding_date_times = models.ManyToManyField(HoldingDateTime)
    question_answers = models.ManyToManyField(QuestionAnswer)
    held = models.BooleanField(default=False)
    early = models.BooleanField(default=False)
    specialized_price = models.ForeignKey(ClassWebinarPrice, on_delete=models.PROTECT, related_name='products')

    # TODO Perform private download links

    def __str__(self):
        return self.title + " (" + str(self.id) + ")"



class ClassProduct(ClassWebinar):
    pass


class WebinarProduct(ClassWebinar):
    pass


class SoldClassWebinar(SoldBasicProduct):
    pass


class SoldClassProduct(SoldClassWebinar):
    pass


class SoldWebinarProduct(SoldClassWebinar):
    pass

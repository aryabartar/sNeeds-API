from ckeditor.fields import RichTextField

from django.db import models

from sNeeds.apps.account.models import (University, FieldOfStudy, Country)
from sNeeds.apps.customAuth.models import CustomUser

STUDY_GRADE_CHOICES = [
    ('college', 'College'),
    ('associate', 'Associate'),
    ('bachelor', 'Bachelor'),
    ('master', 'Master'),
    ('doctoral', 'Doctoral'),
    ('post_doctoral', 'Post Doctoral'),
]


def get_consultant_image_path(instance, filename):
    return "account/images/consultants/{}/image/{}".format(instance.user.id, filename)


def get_consultant_resume_path(instance, filename):
    return "account/files/consultants/{}/resume/{}".format(instance.user.id, filename)


class ConsultantProfileQuerySetManager(models.QuerySet):
    def get_active_consultants(self, **kwargs):
        from sNeeds.apps.store.models import TimeSlotSale
        qs = self.none()
        for obj in self._chain():
            if TimeSlotSale.objects.filter(consultant=obj).exists():
                qs |= ConsultantProfile.objects.filter(id=obj.id)
        return qs


class ConsultantProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        null=True,
        on_delete=models.SET_NULL,
    )
    bio = RichTextField(default="default")
    profile_picture = models.ImageField(upload_to=get_consultant_image_path)
    aparat_link = models.URLField(null=True, blank=True)
    resume = models.FileField(upload_to=get_consultant_resume_path, null=True, blank=True)
    slug = models.SlugField(unique=True, help_text="lowercase pls")
    # universities = models.ManyToManyField(University, blank=True)
    universities = models.ManyToManyField(University, through='StudyInfo',
                                          through_fields=('consultant', 'university'))
    field_of_studies = models.ManyToManyField(FieldOfStudy, blank=True)
    countries = models.ManyToManyField(Country, blank=True)
    active = models.BooleanField(default=True)  # TODO: Check this is working.
    time_slot_price = models.PositiveIntegerField()
    rate = models.FloatField(default=None, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ConsultantProfileQuerySetManager.as_manager()

    def update_rate(self):
        """Currently based on sold time slot sales rate"""
        from sNeeds.apps.comments.models import SoldTimeSlotRate

        sold_time_slot_rate_qs = SoldTimeSlotRate.objects.filter(sold_time_slot__consultant__id=self.id)
        average_rate = sold_time_slot_rate_qs.get_average_rate_or_none()
        self.rate = average_rate
        self.save()

    def __str__(self):
        return self.user.get_full_name()


class UniversityThroughManager(models.QuerySet):

    def filter_consultants(self, params):
        qs = self.all()
        universities = params.get('universities', [])
        if len(universities) != 0:
            qs = qs.filter(university__in=universities)

        field_of_studies = params.get('field_of_studies', [])
        if len(field_of_studies) != 0:
            qs = qs.filter(field_of_study__in=field_of_studies)

        countries = params.get('countries', [])
        if len(countries) != 0:
            qs = qs.filter(country__in=countries)

        grades = params.get('grades', [])
        if len(grades) != 0:
            qs = qs.filter(grade__in=grades)

        result_qs = qs.only('consultant')

        active = params.get('active', [])
        if len(grades) != 0:
            result_qs = result_qs.filter(active__in=active)

        return result_qs


class StudyInfo(models.Model):
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True)
    grade = models.CharField(max_length=64, choices=STUDY_GRADE_CHOICES)

    objects = UniversityThroughManager.as_manager()



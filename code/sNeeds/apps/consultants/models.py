import random

from ckeditor.fields import RichTextField

from django.db import models

from sNeeds.apps.account.models import (University, FieldOfStudy, Country)
from sNeeds.apps.customAuth.models import CustomUser

STUDY_GRADE_CHOICES = [
    ('bachelor', 'Bachelor'),
    ('master', 'Master'),
    ('phd', 'PhD'),
    ('postdoc', 'Post Doc'),
    ('unknown', 'Unknown'),
]


def get_consultant_image_path(instance, filename):
    return "account/images/consultants/{}/image/{}".format(instance.user.id, filename)


def get_consultant_resume_path(instance, filename):
    return "account/files/consultants/{}/resume/{}".format(instance.user.id, filename)


class ConsultantProfileQuerySetManager(models.QuerySet):
    def at_least_one_time_slot(self):
        from sNeeds.apps.store.models import TimeSlotSale
        qs = self.none()
        for obj in self.all():
            if TimeSlotSale.objects.filter(consultant=obj).exists():
                qs |= ConsultantProfile.objects.filter(id=obj.id)
        return qs

    def filter_consultants(self, params):
        qs = self.all()

        if params.get('countries') is not None:
            qs = qs.filter(studyinfo__university__country__id__in=params.get('countries'))
        if params.get('field_of_studies') is not None:
            qs = qs.filter(studyinfo__field_of_study__id__in=params.get('field_of_studies'))
        if params.get('universities') is not None:
            qs = qs.filter(studyinfo__university__id__in=params.get('universities'))
            pass
        return qs


class StudyInfoQueryset(models.QuerySet):
    def with_active_consultants(self):
        qs = self.all().filter(
            consultant__in=list(ConsultantProfile.objects.at_least_one_time_slot())
        )
        return qs


class ConsultantProfile(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.SET_NULL, )
    bio = RichTextField()
    profile_picture = models.ImageField(upload_to=get_consultant_image_path)
    aparat_link = models.URLField(null=True, blank=True)
    resume = models.FileField(upload_to=get_consultant_resume_path, null=True, blank=True)
    slug = models.SlugField(unique=True, help_text="lowercase pls")
    universities = models.ManyToManyField(
        University, through='StudyInfo', through_fields=('consultant', 'university'), blank=True
    )
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


class StudyInfo(models.Model):
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)
    grade = models.CharField(max_length=256, choices=STUDY_GRADE_CHOICES)
    order = models.PositiveIntegerField(help_text="Enter number above 0")

    objects = StudyInfoQueryset.as_manager()

    class Meta:
        ordering = ["order"]
        unique_together = ["consultant", "university", "field_of_study", "grade", "order"]

    def __str__(self):
        return self.consultant.slug + ", " + self.university.name

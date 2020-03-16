from django.db import models

from sNeeds.apps.account.models import get_consultant_image_path, get_consultant_resume_path, University, FieldOfStudy, \
    Country
from sNeeds.apps.customAuth.models import CustomUser


class ConsultantProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        null=True,
        on_delete=models.SET_NULL,
    )
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to=get_consultant_image_path)
    aparat_link = models.URLField(null=True, blank=True)
    resume = models.FileField(upload_to=get_consultant_resume_path, null=True, blank=True)
    slug = models.SlugField(unique=True, help_text="lowercase pls")
    universities = models.ManyToManyField(University, blank=True)
    field_of_studies = models.ManyToManyField(FieldOfStudy, blank=True)
    countries = models.ManyToManyField(Country, blank=True)
    active = models.BooleanField(default=True)  # TODO: Check this is working.
    time_slot_price = models.PositiveIntegerField()
    rate = models.FloatField(default=None, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def update_rate(self):
        """Currently based on sold time slot sales rate"""
        from sNeeds.apps.comments.models import SoldTimeSlotRate

        sold_time_slot_rate_qs = SoldTimeSlotRate.objects.filter(sold_time_slot__consultant__id=self.id)
        average_rate = sold_time_slot_rate_qs.get_average_rate_or_none()
        self.rate = average_rate
        self.save()

    def __str__(self):
        return self.user.get_full_name()

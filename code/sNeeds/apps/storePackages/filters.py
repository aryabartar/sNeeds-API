import django_filters
from django_filters import filters
from django.contrib.contenttypes.models import ContentType

from sNeeds.apps.storePackages.models import SoldStorePackagePhaseDetail

CONTENT_TYPE_FILTER_CHOICES = [
    ('soldstorepaidpackagephase', 'soldstorepaidpackagephase'),
    ('soldstoreunpaidpackagephase', 'soldstoreunpaidpackagephase'),
]


class ContentTypeCharFilter(filters.ChoiceFilter):
    def filter(self, qs, value):
        if value == "soldstorepaidpackagephase":
            qs = qs.filter(
                content_type=ContentType.objects.get(app_label='storePackages', model='soldstorepaidpackagephase')
            )
        elif value == "soldstoreunpaidpackagephase":
            qs = qs.filter(
                content_type=ContentType.objects.get(app_label='storePackages', model='soldstoreunpaidpackagephase')
            )

        return qs


class SoldStorePackagePhaseDetailFilter(django_filters.FilterSet):
    content_type = ContentTypeCharFilter(choices=CONTENT_TYPE_FILTER_CHOICES)

    class Meta:
        model = SoldStorePackagePhaseDetail
        fields = ['object_id']

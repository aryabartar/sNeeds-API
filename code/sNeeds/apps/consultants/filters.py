from django_filters import rest_framework as rest_filters, DateTimeFromToRangeFilter
from django_filters import filters
# from .models import UniversityThrough, ConsultantProfile


# class UniversityFilter(filters.Filter):
#     def filter(self, qs, value):
        # qs2 = UniversityThrough.objects.filter(university_id=value)
        # print("JJLJLJLJLJLJLJLJLJLJLJLJLJLJLJLLJLJLJLJ")
        # print(qs)
        # print('><><><><><<><><><><><><><><><><><><><><><><><><<><><><><><><<')
        # print(qs2)
        # print('><><><><><><><><><><><><><><><><>')
        # qs |= qs2

        # qs = qs.filter(universites=value)
        # return qs
#
#
#
# class ContentTypeCharFilter(filters.ChoiceFilter):
#     def filter(self, qs, value):
#         if value == "soldstorepaidpackagephase":
#             qs = qs.filter(
#                 content_type=ContentType.objects.get(app_label='storePackages', model='soldstorepaidpackagephase')
#             )
#         elif value == "soldstoreunpaidpackagephase":
#             qs = qs.filter(
#                 content_type=ContentType.objects.get(app_label='storePackages', model='soldstoreunpaidpackagephase')
#             )
#
#         return qs


# class ConsultantProfileFilterset(rest_filters.FilterSet):
#     # universities = filters.NumberFilter()
#     universities = UniversityFilter()
#
#     # def filter_universities(self, queryset, name, value):
#     #     queryset = queryset.filter(universities=value)
#
#     class Meta:
#         model = ConsultantProfile

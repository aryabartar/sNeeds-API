from rest_framework import permissions

from sNeeds.apps.account.models import ConsultantProfile
from sNeeds.apps.store.models import SoldTimeSlotSale


class UserFileOwnerPermission(permissions.BasePermission):
    message = "This user is not file owner."

    def has_object_permission(self, request, view, obj):
        user = request.user
        consultant_profile_qs = ConsultantProfile.objects.filter(user=user)

        # Checks if user has bought a time slot from this consultant
        if request.method in permissions.SAFE_METHODS and consultant_profile_qs.exists():
            consultant_profile = consultant_profile_qs.first()
            sold_time_sale_qs = SoldTimeSlotSale.objects.filter(
                consultant=consultant_profile,
            )
            if sold_time_sale_qs.exists():
                return True

        if user == obj.user:
            return True

        return False

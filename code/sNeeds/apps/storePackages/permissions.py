from rest_framework import permissions

from sNeeds.apps.consultants.models import ConsultantProfile


class ConsultantSoldStorePackageAcceptRequestViewPermission(permissions.BasePermission):
    message = "This user has not access to see ConsultantSoldStorePackageAcceptRequest."

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_consultant = ConsultantProfile.objects.filter(user=user).exists()

        if is_consultant:
            consultant = ConsultantProfile.objects.get(user=user)
            return consultant == obj.consultant
        else:
            return user == obj.sold_store_package.sold_to

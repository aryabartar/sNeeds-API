from rest_framework.permissions import BasePermission
from sNeeds.apps.consultants.models import ConsultantProfile


class IsConsultant(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_aithenticated():
            return request.user.is_consultant()
        else:
            return False

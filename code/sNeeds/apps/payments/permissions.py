from rest_framework.permissions import BasePermission
from sNeeds.apps.consultants.models import ConsultantProfile


class IsConsultant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_consultant()

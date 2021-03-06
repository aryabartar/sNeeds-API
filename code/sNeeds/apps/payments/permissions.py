from rest_framework.permissions import BasePermission
from sNeeds.apps.consultants.models import ConsultantProfile


class IsConsultant(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return request.user.is_consultant()
        else:
            return False


class ConsultantDepositInfoOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.consultant.user == request.user:
            return True
        return False

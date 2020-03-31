from rest_framework.permissions import BasePermission, SAFE_METHODS


class PackageFormPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return not user.is_consultant()

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in ['PUT', 'PATCH']:
            if obj.user == user:
                return True
            return False
        else:
            return True

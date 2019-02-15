from rest_framework import permissions
from discounts.models import CafeProfile


class AnonPermissionOnly(permissions.BasePermission):
    """
    For not logged in people!
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class CafeAdminAllowOnly(permissions.BasePermission):
    """
    For not logged in people!
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated :
            return False

        qs = CafeProfile.objects.filter(user__exact=request.user)
        return qs.exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user

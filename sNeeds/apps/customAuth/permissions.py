from rest_framework import permissions


class NotLoggedInPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """
    message = 'You are already authenticates, please log out.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True

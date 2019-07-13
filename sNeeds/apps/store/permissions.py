from rest_framework import permissions


class ConsultantPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """
    message = 'User should be consultant.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        else:
            try:
                request.user.consultant_profile
                return True
            except:
                return False

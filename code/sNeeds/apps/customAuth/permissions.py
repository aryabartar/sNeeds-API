from rest_framework import permissions
from sNeeds.utils.custom.CustomFunctions import get_consultants_interact_with_user


class NotLoggedInPermission(permissions.BasePermission):
    message = 'You are already authenticates, please log out.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True


class SameUserPermission(permissions.BasePermission):
    message = "This user is not the user that is trying to access."

    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False


class StudentDetailedInfoListCreatePermission(permissions.BasePermission):
    message = "Only non consultant users can create StudentDetailedInfo"

    def has_permission(self, request, view):
        user = request.user
        return not user.is_consultant()


class StudentDetailedInfoRetrieveUpdatePermission(permissions.BasePermission):
    message = "Only owner can update and only owner and consultants that service the owner can see info"

    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.user == user:
            return True
        elif request.method == 'GET' and user.is_consultant():
            qs = get_consultants_interact_with_user(obj.user).filter(user__id=user.id)
            return qs.exists()

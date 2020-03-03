from django.db.models import Q

from rest_framework import permissions

from sNeeds.apps.store.models import SoldTimeSlotSale


class ChatOwnerPermission(permissions.BasePermission):
    message = "This user is not in the chat."

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user == obj.user or user == obj.consultant.user:
            return True
        return False


class MessageOwnerPermission(permissions.BasePermission):
    message = "This user is not in the message."

    def has_object_permission(self, request, view, obj):
        user = request.user
        chat = obj.chat

        if user == chat.user or user == chat.consultant.user:
            return True

        return False


# class CanChatPermission(permissions.BasePermission):
#     message = "You don't have permission to see this chat"
#
#     def has_object_permission(self, request, view, obj):
#         request_user = request.user
#         user = obj.user
#         consultant = obj.consultant
#         if request_user == user or request_user == consultant.user:
#             return SoldTimeSlotSale.objects.filter(Q(sold_to=user) & Q(consultant=consultant)).exists()
#         return False
#
#
# class CanSendMessagePermission(permissions.BasePermission):
#     message = "You don't have permission to see this message"
#
#     def has_object_permission(self, request, view, obj):
#         request_user = request.user
#         user = obj.chat.user
#         consultant = obj.chat.consultant
#         if SoldTimeSlotSale.objects.filter(Q(sold_to=user) & Q(consultant=consultant)).exists():
#             return user == request_user or consultant.user == request_user

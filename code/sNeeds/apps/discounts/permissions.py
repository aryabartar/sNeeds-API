from rest_framework import permissions

from sNeeds.apps.carts.models import Cart
from .models import Discount


class CartDiscountPermission(permissions.BasePermission):
    message = "This user is not discount owner."

    # TODO Bug what about GET method? everybody is allowed to get cart discount?
    def has_permission(self, request, view):
        if request.method == "POST":
            cart_id = request.data.get("cart")

            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                return True  # Handled in serializer

            if cart.user == request.user:
                return True
            return False

        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.cart.user:
            return True
        return False


class ConsultantPermission(permissions.BasePermission):
    message = 'User should be consultant.'

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        else:
            return user.is_consultant()


class ConsultantDiscountOwnersPermission(permissions.BasePermission):
    message = 'User should be the creator of discount.'

    def has_object_permission(self, request, view, obj):
        consultants = Discount.objects.get(pk=obj.id).consultants.all()
        consultants_users = [consultant.user for consultant in consultants]
        if request.user in consultants_users and obj.creator == "consultant":
            return True
        return False

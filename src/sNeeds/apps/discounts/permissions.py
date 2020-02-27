from rest_framework import permissions

from sNeeds.apps.carts.models import Cart


class CartConsultantDiscountPermission(permissions.BasePermission):
    message = "This user is not discount owner."

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

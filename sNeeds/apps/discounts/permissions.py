from rest_framework import permissions


class CartConsultantDiscountPermission(permissions.BasePermission):
    message = "This user is not discount owner."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.cart.user:
            return True
        return False

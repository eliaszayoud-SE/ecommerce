from rest_framework.permissions import BasePermission


class IsDeliveryUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff and request.user.is_delivery)
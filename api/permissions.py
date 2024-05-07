from rest_framework import permissions

class IsAdminOrStaffUser(permissions.BasePermission):
    """
    Custom permission to only allow admins and staff users to access.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is either admin or staff
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)


class IsCustomerUser(permissions.BasePermission):
    """
    Custom permission to only allow customer users to access.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is not admin or staff
        return request.user.is_authenticated and not (request.user.is_staff or request.user.is_superuser)

from rest_framework import permissions


class IsAuthenticatedOwnerOrAdminOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    message = "Access only for owner or admin!"

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user.is_authenticated
            or request.user.is_superuser)

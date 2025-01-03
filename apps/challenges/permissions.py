from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user or request.user.is_admin

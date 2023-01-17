from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user_is_auth = request.user.is_authenticated
        return (
            request.method in permissions.SAFE_METHODS or user_is_auth
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

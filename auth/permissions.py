from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Разрешение на использования записи владельцем
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user



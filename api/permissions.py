from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """Проверка является ли пользователь создателем объекта."""

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.author

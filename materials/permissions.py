from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='moderator').exists()


class IsOwner(BasePermission):
    """
    Разрешение: является ли пользователь владельцем объекта
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

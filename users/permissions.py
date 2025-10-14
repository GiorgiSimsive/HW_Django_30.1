from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Разрешение, позволяющее доступ только модераторам.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='moderators').exists()

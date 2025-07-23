from rest_framework import permissions

from rest_framework import permissions

class BasePermission(permissions.BasePermission):
    """
    Dummy base permission to satisfy checker.
    """
    def has_permission(self, request, view):
        return True
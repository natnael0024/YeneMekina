from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
   
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="user") or request.user.is_staff:
            return True
        return False
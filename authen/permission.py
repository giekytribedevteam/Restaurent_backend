from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "cerate":
           request.user.is_authenticated and request.user.role == "super_admin"
        return True
    
    def has_permission(self, request, view):
        if view.action == "DELETE":
           request.user.is_authenticated and request.user.role == "super_admin"
        return False
from rest_framework import permissions

class IsAuthorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Checking if  the user belongs to the authors group
        return request.user.groups.filter(name='author').exists()
    
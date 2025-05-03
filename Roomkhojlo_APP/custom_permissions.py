from rest_framework.permissions import BasePermission
class IsAuthenticatedEmployee(BasePermission):
    """
    Allows access only to authenticated users with role='employee' and is_active=True.
    """
    def has_permission(self, request, view):
        user = request.user
        print(user)  
        return (
            user.is_authenticated and
            user.is_active and
            hasattr(user, 'role') and
            user.role == 'employee'
        )
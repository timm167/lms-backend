from rest_framework.permissions import BasePermission

class IsSelfStudentOrAdmin(BasePermission):
    """
    Custom permission to allow students and admins to view, create, update, or delete enrollments.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view based on their role.
        """
        # Ensure the user is authenticated, and allow students or admins to access the view
        return request.user.is_authenticated and (
            request.user.role == 'student' or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform actions on a specific object.
        """
        # For GET, PUT, PATCH, DELETE, students can only access their own enrollments
        # Admins can access any enrollment
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            return obj.student.user == request.user or request.user.is_staff
        
        # Default case: deny access for unsupported methods
        return False

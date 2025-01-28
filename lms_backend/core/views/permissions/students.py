from rest_framework.permissions import BasePermission

class IsStudentOrAdmin(BasePermission):
    """
    Custom permission to allow students and admins to view, create, update, or delete enrollments.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view based on their role and request type.
        """
        # Allow students and admins to create enrollments (POST request)
        if request.method == 'POST':
            return request.user.is_authenticated and (
                request.user.role == 'student' or request.user.is_staff
            )
        
        # For other methods (GET, PUT, PATCH, DELETE), ensure the user is authenticated
        return request.user.is_authenticated and (
            request.user.role == 'student' or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform actions on a specific object.
        """
        # For GET (viewing an enrollment) or DELETE (deleting an enrollment), we check the ownership of the object.
        if request.method == 'GET':
            # Students can only view their own enrollment; admins can view any
            return obj.student.user == request.user or request.user.is_staff
        
        if request.method == 'DELETE':
            # Students can delete their own enrollment; admins can delete any
            return obj.student.user == request.user or request.user.is_staff
        
        # For PUT and PATCH (update operations), students can update their own enrollments; admins can update any
        if request.method in ['PUT', 'PATCH']:
            return obj.student.user == request.user or request.user.is_staff
        
        # Default case: allow admin access to any object
        return request.user.is_authenticated and request.user.is_staff

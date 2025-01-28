from rest_framework import permissions

class IsSelfTeacherOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow access to lessons/courses for teachers and admins.
    Teachers can manage lessons and courses, and admins can do everything.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view based on their role.
        """
        # Allow both teachers and admins to access the view
        return request.user.is_authenticated and (
            request.user.role == 'teacher' or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform actions on a specific object.
        """
        # If the request method is GET, PUT, PATCH, or DELETE, teachers and admins can access/manage the object
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            return request.user.is_authenticated and (
                request.user.role == 'teacher' or request.user.is_staff
            )
        
        # Default: deny access for unsupported methods
        return False

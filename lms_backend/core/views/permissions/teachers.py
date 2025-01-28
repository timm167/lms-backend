from rest_framework import permissions

class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow teachers and admins to access certain views.
    Teachers can create lessons and courses, and admins can do everything.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view based on their role.
        """
        # For POST (creating lessons and courses), only allow teachers and admins
        if request.method == 'POST':
            return request.user.is_authenticated and (
                request.user.role == 'teacher' or request.user.is_staff
            )
        
        # For other methods (GET, PUT, PATCH, DELETE), allow teachers and admins
        return request.user.is_authenticated and (
            request.user.role == 'teacher' or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform actions on a specific object.
        """
        # For GET (viewing an object), teachers and admins can access the data
        if request.method == 'GET':
            return request.user.is_authenticated and (
                request.user.role == 'teacher' or request.user.is_staff
            )
        
        # For DELETE (deleting an object), only teachers and admins can delete lessons/courses
        if request.method == 'DELETE':
            return request.user.is_authenticated and (
                request.user.role == 'teacher' or request.user.is_staff
            )
        
        # For PUT or PATCH (updating an object), only teachers and admins can update lessons/courses
        if request.method in ['PUT', 'PATCH']:
            return request.user.is_authenticated and (
                request.user.role == 'teacher' or request.user.is_staff
            )
        
        return False  # Default: deny access if the method doesn't match any of the conditions

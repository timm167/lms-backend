from rest_framework import permissions

class IsStudentOrTeacherOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow students, teachers, and admins to access the view.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view based on their role and request type.
        """
        # For POST (creating), allow students, teachers, and admins to create
        if request.method == 'POST':
            return request.user.is_authenticated and (
                request.user.role == 'student' or request.user.role == 'teacher' or request.user.is_staff
            )
        
        # For other methods (GET, PUT, PATCH, DELETE), allow students, teachers, and admins
        return request.user.is_authenticated and (
            request.user.role == 'student' or request.user.role == 'teacher' or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform actions on a specific object.
        """
        # For GET (viewing an object)
        if request.method == 'GET':
            return request.user.is_authenticated and (
                obj.student.user == request.user or 
                obj.course.instructor == request.user or 
                request.user.is_staff
            )

        # For DELETE (deleting an object), students can delete their own enrollments, 
        # teachers can delete enrollments from their courses, admins can delete any enrollment.
        if request.method == 'DELETE':
            return request.user.is_authenticated and (
                obj.student.user == request.user or 
                obj.course.instructor == request.user or 
                request.user.is_staff
            )

        # For PUT or PATCH (updating an object), students can update their own enrollment, 
        # teachers can update enrollments in their courses, admins can update any enrollment.
        if request.method in ['PUT', 'PATCH']:
            return request.user.is_authenticated and (
                obj.student.user == request.user or 
                obj.course.instructor == request.user or 
                request.user.is_staff
            )

        # Default case: Allow admin to access and modify any object
        return request.user.is_authenticated and request.user.is_staff

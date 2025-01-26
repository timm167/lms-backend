from rest_framework import permissions
from rest_framework.permissions import BasePermission

# Custom permission classes

class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow teachers and admins to create lessons and courses.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'teacher') or request.user.is_staff
    
class IsStudentOrAdmin(BasePermission):
    """
    Custom permission to only allow students and admins to create enrollments.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            # Allow both students and admins to create enrollments
            return request.user.is_authenticated and ((request.user.role == 'student')  or request.user.is_staff)
        # Allow only students and admins to access the view
        return request.user.is_authenticated and (request.user.role == 'student' or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        # Allow students to view and delete their own enrollments
        if request.method in ['GET', 'DELETE']:
            return obj.student.user == request.user or request.user.is_staff
        return request.user.is_authenticated and request.user.is_staff
     

class IsStudentOrTeacherOrAdmin(BasePermission):
    """
    Custom permission to only allow students, teachers, and admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'student' or request.user.role == 'teacher' or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (obj.student.user == request.user or obj.course.instructor == request.user or request.user.is_staff)


from rest_framework import permissions

class IsSelfTeacherOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'teacher' or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'DELETE']:
            return request.user.is_authenticated and (
                request.user.role == 'teacher' or request.user.is_staff
            )
        return False

class IsStudentOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
            
            return request.user.is_authenticated and (
                 request.user.role == 'student' or request.user.is_staff)



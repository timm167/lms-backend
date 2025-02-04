from rest_framework.permissions import BasePermission

class IsSelfStudentOrAdmin(BasePermission):

    def has_permission(self, request, view):

        return request.user.is_authenticated and (
            request.user.role == 'student' or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):

        if request.method in ['GET','DELETE']:
            return obj.student.user == request.user or request.user.is_staff
        
        return False

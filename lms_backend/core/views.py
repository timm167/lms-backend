from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions

from rest_framework import generics
from core.models import User, Student, Teacher, Course, Lesson, Assignment, Enrollment
from core.serializers import (
    UserSerializer,
    StudentSerializer,
    TeacherSerializer,
    CourseSerializer,
    LessonSerializer,
    AssignmentSerializer,
    EnrollmentSerializer,
)

## Custom Permissions
def user_view_only_permissions(self):
    if self.request.method == 'DELETE':

        return [IsTeacherOrAdmin()]
    elif self.request.method == 'PUT' or self.request.method == 'PATCH':

        return [IsTeacherOrAdmin()]

    return [IsAuthenticated()]


def teacher_student_view_only_permissions(self):
    if self.request.method == 'DELETE':

        return [IsTeacherOrAdmin()]
    elif self.request.method == 'PUT' or self.request.method == 'PATCH':

        return [IsTeacherOrAdmin()]

    return [IsAuthenticated()]

## Custom permission classes
class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow teachers and admins to create lessons and courses.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'teacher') or request.user.is_staff


## -- CRUD Permissions -- ##

# Users
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


# Students
class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]


# Teachers
class TeacherListCreateView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUser]


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    
    def get_permissions(self):
        return teacher_student_view_only_permissions(self)

# Courses
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrAdmin]


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        return user_view_only_permissions(self)

#Lessons
class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrAdmin]


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    
    def get_permissions(self):
        return user_view_only_permissions(self)

# Assignments
class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsTeacherOrAdmin]


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        return user_view_only_permissions(self)
    
# Enrollments
class EnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAdminUser]


class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsTeacherOrAdmin]

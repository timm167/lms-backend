from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
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

# Custom permission classes

class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow teachers and admins to create lessons and courses.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'teacher') or request.user.is_staff
    
class IsStudentOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow students and admins to create lessons and courses.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.role == 'student'
        return request.user.is_authenticated and (request.user.role == 'student' or request.user.is_staff)
         
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.method == 'DELETE':
            return obj.student.user == request.user or request.user.is_staff
        return request.user.is_authenticated and request.user.is_staff
    

# CRUD Permissions for Views

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
        if self.request.method in ['DELETE']:
            return [IsAdminUser()]
        if self.request.method in ['PUT', 'PATCH']:
            return [IsTeacherOrAdmin()]
        return [IsAuthenticated()] 

# Courses
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrAdmin]

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [IsTeacherOrAdmin()]
        return [IsAuthenticated()]

# Lessons
class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrAdmin]

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [IsTeacherOrAdmin()]
        return [IsAuthenticated()]

# Assignments
class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsTeacherOrAdmin]

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [IsTeacherOrAdmin()]
        return [IsAuthenticated()]

# Enrollments
class EnrollmentListCreateView(generics.ListCreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudentOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.all()
        return Enrollment.objects.filter(student__user=user)

    def perform_create(self, serializer):
        # Set the student to the current user
        serializer.save(student=self.request.user.student)

class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [IsStudentOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.all()
        return Enrollment.objects.filter(student__user=user)

from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS, BasePermission
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
        elif user.role == 'teacher':
            return Enrollment.objects.filter(course__instructor=user.teacher)
        return Enrollment.objects.filter(student__user=user)

    def perform_create(self, serializer):
        if self.request.user.role == 'teacher':
            self.permission_denied(self.request, message="Only students and admins can create enrollments.")
        elif self.request.user.role == 'student':
            student = serializer.validated_data['student']
            if student.user == self.request.user:
                serializer.save(student=self.request.user.student)
        elif self.request.user.is_staff:
            serializer.save()

class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_permissions(self):
        if self.request.method in [ 'PUT', 'PATCH']:
            return [IsAdminUser()]
        if self.request.method in ['DELETE']:
            return [IsStudentOrAdmin()]
        return [IsStudentOrTeacherOrAdmin()]

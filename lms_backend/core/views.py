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

from core.permissions import IsTeacherOrAdmin, IsStudentOrAdmin, IsStudentOrTeacherOrAdmin

# CRUD Permissions for Views

# Users
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        print("Request received in ProtectedView")
        print("Authorization header:", request.headers.get('Authorization'))
        return super().get(request, *args, **kwargs)

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

    def perform_create(self, serializer):
        print("creating lesson")
        course = Course.objects.get(id=self.request.data.get('course_id'))
        Lesson.objects.create_lesson(
            course=course,
            title=self.request.data.get('title'),
            content=self.request.data.get('content'),
            lesson_no=self.request.data.get('lesson_no'),
            video_url=self.request.data.get('video_url')
        )

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

from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from core.models import User, Student, Teacher, Admin
from core.serializers import UserSerializer, StudentSerializer, TeacherSerializer, AdminSerializer
from .permissions.students_permissions import IsSelfStudentOrAdmin
from .permissions.teachers_permissions import IsSelfTeacherOrAdmin

#------------------------------------------------------------#
# Users
#------------------------------------------------------------#

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


#------------------------------------------------------------#
# Students
#------------------------------------------------------------#

class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsSelfStudentOrAdmin]

#------------------------------------------------------------#
# Teachers
#------------------------------------------------------------#

class TeacherListView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUser]

class TeacherDetailView(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsSelfTeacherOrAdmin]

#------------------------------------------------------------#
# Admins
#------------------------------------------------------------#

class AdminListView(generics.ListAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser]

class AdminDetailView(generics.RetrieveAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser]
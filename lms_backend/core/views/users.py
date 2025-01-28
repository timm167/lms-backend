from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from core.models import User, Student, Teacher, Admin
from core.serializers import UserSerializer, StudentSerializer, TeacherSerializer
from .permissions import IsSelfTeacherOrAdmin, IsSelfStudentOrAdmin

#------------------------------------------------------------#
# Users
#------------------------------------------------------------#

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


#------------------------------------------------------------#
# Students
#------------------------------------------------------------#

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsSelfStudentOrAdmin]


#------------------------------------------------------------#
# Teachers
#------------------------------------------------------------#

class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsSelfTeacherOrAdmin]

#------------------------------------------------------------#
# Admins
#------------------------------------------------------------#

class AdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Admin.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
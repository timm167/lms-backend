from rest_framework import serializers
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
    

#------------------------------------------------------------#

from ..models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    from .courses import CourseSerializer
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    id = serializers.IntegerField(source='user.id')
    teaching_courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'email', 'first_name', 'last_name', 'teaching_courses']

#------------------------------------------------------------#

from ..models import Student

class StudentSerializer(serializers.ModelSerializer):
    from .courses import CourseSerializer   
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    id = serializers.IntegerField(source='user.id')
    enrolled_courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name', 'last_name', 'enrolled_courses']

#------------------------------------------------------------#

from ..models import Admin

class AdminSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    id = serializers.IntegerField(source='user.id')

    class Meta:
        model = Admin
        fields = ['id', 'email', 'first_name', 'last_name', 'is_staff']

#------------------------------------------------------------#

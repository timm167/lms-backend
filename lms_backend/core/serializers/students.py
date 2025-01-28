from core.models import Student
from rest_framework import serializers

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
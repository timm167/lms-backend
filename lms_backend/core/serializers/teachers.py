from core.models import Teacher
from rest_framework import serializers

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
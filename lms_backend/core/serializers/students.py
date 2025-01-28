from core.models import Student
from rest_framework import serializers

class StudentSerializer(serializers.ModelSerializer):
    enrolled_courses = serializers.SerializerMethodField()
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    id = serializers.IntegerField(source='user.id')

    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name', 'last_name', 'enrolled_courses']

    def get_courses(self, obj):
        from .courses import CourseDisplaySerializer
        return CourseDisplaySerializer(obj.courses.all(), many=True).data

#------------------------------------------------------------#
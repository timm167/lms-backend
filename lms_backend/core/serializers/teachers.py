from core.models import Teacher
from rest_framework import serializers


class TeacherSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    id = serializers.IntegerField(source='user.id')
    teaching_courses = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'email', 'first_name', 'last_name', 'teaching_courses']

    def get_teaching_courses(self, obj):
        from .courses import CourseDisplaySerializer
        return CourseDisplaySerializer(obj.courses.all(), many=True).data

#------------------------------------------------------------#
from rest_framework import serializers
from core.models import Course
from .users_serializers import UserDisplaySerializer
from .course_objects_serializers import AssignmentDisplaySerializer, LessonDisplaySerializer

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserDisplaySerializer()  
    students = UserDisplaySerializer(many=True)
    lessons = LessonDisplaySerializer(many=True)
    assignments = AssignmentDisplaySerializer(many=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
            'description', 
            'teacher', 
            'students', 
            'lessons', 
            'assignments', 
        ]


class CourseDisplaySerializer(serializers.ModelSerializer):    
    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
        ]

class BrowseCourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
            'description', 
            'teacher_name', 
        ]

    def get_teacher_name(self, obj):
        return f"{obj.teacher.user.first_name} {obj.teacher.user.last_name}"
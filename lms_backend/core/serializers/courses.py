from rest_framework import serializers
from core.models import Course
from .users import UserDisplaySerializer
from .course_objects import AssignmentDisplaySerializer, LessonDisplaySerializer

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserDisplaySerializer()  
    students = UserDisplaySerializer(many=True)
    lessons = LessonDisplaySerializer(many=True)
    assignments = AssignmentDisplaySerializer(many=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
            'description', 
            'instructor', 
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
from rest_framework import serializers
from core.models import Course
from .users import StudentSerializer, TeacherSerializer
from .course_objects import LessonSerializer, AssignmentSerializer

class CourseSerializer(serializers.ModelSerializer):
    instructor = TeacherSerializer()  
    students = StudentSerializer(many=True)  
    assignments = AssignmentSerializer(many=True) 
    lessons = LessonSerializer(many=True) 
    
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


class CourseDisplaySerialzer(serializers.ModelSerializer):    
    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
        ]
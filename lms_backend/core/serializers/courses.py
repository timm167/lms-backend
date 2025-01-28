from rest_framework import serializers
from ..models import Lesson, Assignment, Course, Teacher, Student

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'lesson_no', 'video_url']

    # I can't remember why I did this. 
    # It might be obsolete I need to investigate.

    def create(self, validated_data):
        course = validated_data.get('course')
        title = validated_data.get('title')
        content = validated_data.get('content')
        lesson_no = validated_data.get('lesson_no')
        video_url = validated_data.get('video_url')
        
        lesson = Lesson.objects.create(
            course=course,
            title=title,
            content=content,
            lesson_no=lesson_no,
            video_url=video_url
        )
        return lesson

#-----------------------------------------------------------#


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'title', 'description', 'due_date', 'max_score', 'pass_score']

#-----------------------------------------------------------#


class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
    assignments = serializers.PrimaryKeyRelatedField(queryset=Assignment.objects.all(), many=True)
    lessons = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), many=True)
    
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


#-----------------------------------------------------------#
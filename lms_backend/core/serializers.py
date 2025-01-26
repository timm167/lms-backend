from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']

#------------------------------------------------------------#

from .models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'teaching_courses']

#------------------------------------------------------------#

from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    enrolled_courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'enrolled_courses']

#------------------------------------------------------------#

from .models import Admin

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = ['id', 'user']

#------------------------------------------------------------#

from .models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'lesson_no', 'video_url']

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

from .models import Assignment

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'title', 'description', 'due_date', 'max_score', 'pass_score']

#-----------------------------------------------------------#

from .models import Course

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

from .models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date', 'completed']
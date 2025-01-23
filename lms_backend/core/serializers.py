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
            'duration_weeks', 
            'start_date', 
            'end_date'
        ]


#-----------------------------------------------------------#

from .models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    course = CourseSerializer()
    lessons_completed = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), many=True)
    assignments_completed = serializers.PrimaryKeyRelatedField(queryset=Assignment.objects.all(), many=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date', 'completed', 'lessons_completed', 'assignments_completed']
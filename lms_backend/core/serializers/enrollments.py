from rest_framework import serializers
from core.models import Student, Course, Enrollment
from .courses import CourseSerializer
from .users import StudentSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date', 'completed']
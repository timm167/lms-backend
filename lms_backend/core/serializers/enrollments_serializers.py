from rest_framework import serializers
from core.models import Student, Course, Enrollment
from .courses_serializers import CourseDisplaySerializer
from .users_serializers import UserDisplaySerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserDisplaySerializer()
    course = CourseDisplaySerializer()
    enrollment_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date', 'completed']
from rest_framework import serializers
from core.models import Student, Course, Enrollment
from .courses import CourseDisplaySerializer
from .users import UserDisplaySerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserDisplaySerializer()
    course = CourseDisplaySerializer()
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date', 'completed']
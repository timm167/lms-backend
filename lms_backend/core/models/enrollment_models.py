from django.db import models
from .user_models import Student
from .course_models import Course

# A model to represent a student's enrollment in a course
class Enrollment(models.Model):
    student = models.ForeignKey(Student, related_name="enrollments", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="enrollments_in_course", on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"

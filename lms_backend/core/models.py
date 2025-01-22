from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CourseManager, StudentManager, TeacherManager, AdminManager

# Model notes:
# - The User model is a subclass of Django’s AbstractUser model.
# - The Student, Teacher, and Admin models are subclasses of User.
# - The Course model represents a course in the LMS.
# - The Lesson model represents a lesson within a course.
# - The Assignment model represents an assignment within a course.
# - The Enrollment model represents a student's enrollment in a course.

# Field types:
# - OneToOneField means that each user can have only one corresponding student, teacher, or admin.
# - ManyToManyField means that a user can be enrolled in multiple courses, and a course can have multiple students.
# - CharField is a field for storing text data.
# - TextField is a field for storing longer text data.
# - ForeignKey is a field for creating a many-to-one relationship with another model. i.e. Many lessons can belong to one course.
# - URLField is a field for storing URLs.
# - DateTimeField is a field for storing date and time data.
# - IntegerField is a field for storing integer data.

# Other notes:
# - Use cascade delete for related models to ensure data integrity.
# - Use set null as I don't want to delete the course if the instructor is deleted. (Not sure exactly how to handle this yet)

# Future models:
# - Add a model for storing student grades.
# - Add a model for storing student submissions.
# - Add a model for storing cross-course materials.
# - Add a model for storing completed courses.
# - Each enrollment should track the student's progress in the course.

#------------------------------------------------------------#
# User models
#------------------------------------------------------------#

# Base class User: Contains common user properties
class User(AbstractUser):
    pass

# Subclass Student: Specific functionality for students
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrolled_courses = models.ManyToManyField('Course', related_name='students', blank=True)
    objects = StudentManager()

    def __str__(self):
        return self.user.username

# Subclass Teacher: Specific functionality for teachers
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teaching_courses = models.ManyToManyField('Course', related_name='teachers', blank=True)
    objects = TeacherManager()

    def __str__(self):
        return self.user.username


# Subclass Admin: Specific functionality for admins
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    objects = AdminManager()
    
    def __str__(self):
        return f"{self.user.username} ({self.role})"


#------------------------------------------------------------#
# Course models
#------------------------------------------------------------#

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(Teacher, related_name="courses_taught", on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField(Student, related_name="courses_enrolled", blank=True)
    lessons = models.ManyToManyField("Lesson", related_name="courses", blank=True)
    assignments = models.ManyToManyField("Assignment", related_name="courses", blank=True)
    duration_weeks = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    objects = CourseManager()

    def __str__(self):
        return self.title

# A lesson within a course
class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    lesson_no = models.IntegerField() 
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

# An assignment within a course
class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name="assignments", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.IntegerField()
    pass_score = models.IntegerField()

    def __str__(self):
        return self.title

# A model to represent a student's enrollment in a course
class Enrollment(models.Model):
    student = models.ForeignKey(Student, related_name="enrollments", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="enrollments", on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    lessons_completed = models.ManyToManyField(Lesson, related_name="completed_by", blank=True)
    assignments_completed = models.ManyToManyField(Assignment, related_name="completed_by", blank=True)
    
    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"


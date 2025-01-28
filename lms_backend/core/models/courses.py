from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from ..managers.managers import CourseManager, StudentManager, TeacherManager, AdminManager, UserManager
from .users import Student, Teacher, Admin, User

# Course models
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(Teacher, related_name="courses_taught", on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField("Student", related_name="courses_enrolled", blank=True)
    lessons = models.ManyToManyField("Lesson", related_name="courses_with_lessons", blank=True)
    assignments = models.ManyToManyField("Assignment", related_name="courses_with_assignments", blank=True)
    objects = CourseManager()

    def __str__(self):
        return self.title


# A lesson within a course
class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons_in_course", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    lesson_no = models.IntegerField(null=True, blank=True) 
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    


# An assignment within a course
class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name="assignments_in_course", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    max_score = models.IntegerField(null=True, blank=True)
    pass_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
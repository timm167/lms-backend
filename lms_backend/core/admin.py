from django.contrib import admin
from .models import User, Student, Teacher, Admin, Course, Lesson, Assignment, Enrollment

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Assignment)
admin.site.register(Enrollment)
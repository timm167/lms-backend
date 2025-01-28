from django.contrib import admin
from ..models import User, Student, Teacher, Admin, Course, Lesson, Assignment, Enrollment

## I don't think anything else needs to be done here. 
## The default admin interface won't be used anyway as I will serve API endpoints to React app.

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Assignment)
admin.site.register(Enrollment)
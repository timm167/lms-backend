from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from core.managers import UserManager

#------------------------------------------------------------#
# User models
#------------------------------------------------------------#

# User model: AbstractBaseUser subclass
class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def is_admin(self):
        return self.role == 'admin'

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser 

    def has_module_perms(self, app_label):
        return self.is_superuser 

    def __str__(self):
        return f"{self.username} ({self.role})"


# Linked Object: Specific functionality for students
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrolled_courses = models.ManyToManyField('Course', related_name='students_in_course', blank=True)

    def __str__(self):
        return self.user.username


# Linked Object: Specific functionality for teachers
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teaching_courses = models.ManyToManyField('Course', related_name='teachers_in_course', blank=True)

    def __str__(self):
        return self.user.username


# Linked Object:  Specific functionality for admins
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    is_staff = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.user.role})"







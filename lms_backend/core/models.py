from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CourseManager, StudentManager, TeacherManager, AdminManager, UserManager, LessonManager, AssignmentManager


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

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)  
        super().save(*args, **kwargs)
        if not self.pk:  
            if self.role == 'student' and not hasattr(self, 'student'):
                Student.objects.get_or_create(user=self)
            elif self.role == 'teacher' and not hasattr(self, 'teacher'):
                Teacher.objects.get_or_create(user=self)
            elif self.role == 'admin' and not hasattr(self, 'admin'):
                Admin.objects.get_or_create(user=self)


        

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


# Subclass Student: Specific functionality for students
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrolled_courses = models.ManyToManyField('Course', related_name='students_in_course', blank=True)
    objects = StudentManager()

    def __str__(self):
        return self.user.username


# Subclass Teacher: Specific functionality for teachers
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teaching_courses = models.ManyToManyField('Course', related_name='teachers_in_course', blank=True)
    objects = TeacherManager()

    def __str__(self):
        return self.user.username


# Subclass Admin: Specific functionality for admins
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    objects = AdminManager()
    is_staff = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.user.role})"


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
    objects = LessonManager()

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
    objects = AssignmentManager()

    def __str__(self):
        return self.title


# A model to represent a student's enrollment in a course
class Enrollment(models.Model):
    student = models.ForeignKey(Student, related_name="enrollments", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="enrollments_in_course", on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"

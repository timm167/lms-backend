from django.db import models
from django.contrib.auth.models import BaseUserManager


# Manager for the User model
class UserManager(BaseUserManager):

    def create_user(self, username, password=None, role='student', **extra_fields):
        """
        Create and return a regular user.
        """
        if not username:
            raise ValueError('The username must be set')
        if not password:
            raise ValueError('The password must be set')

        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and return a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, role='admin', **extra_fields)

# Manager for the Course model
class CourseManager(models.Manager):
    def enroll_student(self, student):
        """Enroll a student in the course."""
        self.students.add(student) 
        print(f"{student.username} enrolled in {self.title}.")

    def unenroll_student(self, student):
        from .models import Enrollments
        """Unenroll a student from the course."""
        self.students.remove(student)
        Enrollments.objects.filter(student=student, course=self).delete()
        print(f"{student.username} unenrolled from {self.title}.")

    def add_teacher(self, teacher):
        """Add a teacher to the course."""
        self.teachers.add(teacher)
    
    def remove_teacher(self, teacher):
        """Remove a teacher from the course."""
        self.teachers.remove(teacher)
    
    def add_lesson(self, lesson):
        """Add a lesson to the course."""
        self.lessons.add(lesson)
    
    def remove_lesson(self, lesson):
        """Remove a lesson from the course."""
        self.lessons.remove(lesson)
    
    def add_assignment(self, assignment):
        """Add an assignment to the course."""
        self.assignments.add(assignment)
    
    def remove_assignment(self, assignment):
        """Remove an assignment from the course."""
        self.assignments.remove(assignment)

    actions = ['enroll_student', 'unenroll_student', 'add_teacher', 'remove_teacher', 'add_lesson', 'remove_lesson', 'add_assignment', 'remove_assignment']
    
# Manager for the Student model
class StudentManager(models.Manager):
    
    def browse_courses(self):
        from .models import Course
        """Return a list of all available courses."""
        return Course.objects.all()

    def enroll_in_course(self, course):
        """Enroll the student in a course."""
        self.enrolled_courses.add(course)
        course.enroll_student(self)  
        return f"{self.user.username} has been enrolled in {course.title}"

    def unenroll_from_course(self, course):
        """Unenroll the student from a course."""
        self.enrolled_courses.remove(course)
        course.unenroll_student(self)  
        return f"{self.user.username} has been unenrolled from {course.title}"

    def list_enrolled_courses(self):
        """Return the list of courses the student is enrolled in."""
        return self.enrolled_courses.all()
    
    def delete_user(self):
        """Delete the student's user account."""
        self.user.delete()
        return f"{self.user.username} has been deleted."
    

class AdminManager(models.Manager):
    def create_course(self, title, description, instructor):
        from .models import Course
        """Create a course and assign an instructor."""
        course = Course.objects.create(
            title=title, 
            description=description, 
            instructor=instructor
        )
        return course

    def create_user(self, username, password, role, **extra_fields):
        from .models import User, Student, Teacher, Admin
        """Create a new user (student, teacher, or admin)."""
        user = User.objects.create_user(username=username, password=password)
        if role == 'student':
            Student.objects.create(user=user)
        elif role == 'teacher':
            Teacher.objects.create(user=user)
        elif role == 'admin':
            Admin.objects.create(user=user, is_staff=True)
        return user
    

class TeacherManager(models.Manager):

    def create_lesson(self, course, title, content, lesson_no):
        from .models import Lesson
        """Create a lesson and add it to the course."""
        lesson = Lesson.objects.create(course=course, title=title, content=content, lesson_no=lesson_no)
        course.add_lesson(lesson) 
        return lesson

    def create_assignment(self, course, title, description, due_date, max_score, pass_score):
        from .models import Assignment
        """Create an assignment for a course."""
        assignment = Assignment.objects.create(
            course=course,
            title=title,
            description=description,
            due_date=due_date,
            max_score=max_score,
            pass_score=pass_score
        )
        course.add_assignment(assignment) 
        return assignment

    def add_lesson(self, course, lesson):
        """Add a lesson to the course."""
        course.lessons.add(lesson)
    
    def remove_lesson(self, course, lesson):
        """Remove a lesson from the course."""
        course.lessons.remove(lesson)

    def add_assignment(self, course, assignment):
        """Add an assignment to the course."""
        course.assignments.add(assignment)
    
    def remove_assignment(self, course, assignment):
        """Remove an assignment from the course."""
        course.assignments.remove(assignment)

    def create_course(self, title, description):
        from .models import Course
        """Create a course and assign the teacher."""
        course = Course.objects.create(
            title=title,
            description=description,
            instructor=self
        )
        self.teaching_courses.add(course)
        return course
    
class LessonManager(models.Manager):
    def create_lesson(self, course, title, content, lesson_no, video_url):
        """Create a lesson and add it to the course."""
        lesson = self.create(course=course, title=title, content=content, lesson_no=lesson_no, video_url=video_url)
        course.lessons.add(lesson)
        return lesson
    
    
class AssignmentManager(models.Manager):
    def create_assignment(self, course, title, description, due_date, max_score, pass_score):
        """Create an assignment for a course."""
        assignment = self.create(
            course=course,
            title=title,
            description=description,
            due_date=due_date,
            max_score=max_score,
            pass_score=pass_score
        )
        course.add_assignment(assignment)
        return assignment
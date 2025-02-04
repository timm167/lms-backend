from django.db import models

#------------------------------------------------------------#
# Manager for the Course model
#------------------------------------------------------------#

class CourseManager(models.Manager):

    #------------------------------------------------------------#
    # Create/Delete Course
    #------------------------------------------------------------#

    def create_course(self, title, description, teacher):
        from core.models import Course
        course = Course.objects.create(title=title, description=description, teacher=teacher)
        return course
    
    def delete_course(self, course):
        course.delete()


    #------------------------------------------------------------#
    # Lessons
    #------------------------------------------------------------#

    def create_lesson(self, course, title, content, lesson_no):
        from core.models import Lesson
        lesson = Lesson.objects.create(course=course, title=title, content=content, lesson_no=lesson_no)
        course.add_lesson(lesson) 
        return lesson
    
    def delete_lesson(self, lesson):
        self.lessons.remove(lesson)
        lesson.delete()
    

    #------------------------------------------------------------#
    # Assignments
    #------------------------------------------------------------#

    def create_assignment(self, course, title, description, due_date, max_score, pass_score):
        from core.models import Assignment
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
    
    def delete_assignment(self, assignment):
        self.assignments.remove(assignment)
        assignment.delete()


    #------------------------------------------------------------#
    # Enrollments
    #------------------------------------------------------------#    
    
    def enroll_student(self, course, student):
        course.students.add(student) 
        course.save()

    def unenroll_student(self,course, student):
        from core.models import Enrollment
        course.students.remove(student)
        Enrollment.objects.filter(student=student, course=course).delete()


    #------------------------------------------------------------#
    # Add/Remove Teachers
    #------------------------------------------------------------#
    
    def add_teacher(self, course, teacher):
        course.teacher = teacher
        teacher.teaching_courses.add(course)
        course.save()
    
    # NOT IN USE
    def remove_teacher(self, course, teacher):
        course.teacher = None
        teacher.teaching_courses.remove(course)
        course.save()
    



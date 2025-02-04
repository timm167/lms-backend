from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from core.models import Teacher, Student, Admin, Assignment, Lesson, Course, Enrollment

# Update the course whenever a lesson or assignment is added or deleted
@receiver(post_save, sender=Assignment)
def update_assignment(sender, instance, **kwargs):
    instance.course.assignments.add(instance)

@receiver(post_save, sender=Lesson)
def update_lesson(sender, instance, **kwargs):
    instance.course.lessons.add(instance)

@receiver(post_delete, sender=Assignment)
def delete_assignment(sender, instance, **kwargs):
    instance.course.assignments.remove(instance)

@receiver(post_delete, sender=Lesson)
def delete_lesson(sender, instance, **kwargs):
    instance.course.lessons.remove(instance)

# When a course is deleted, delete all lessons and assignments associated with it
@receiver(post_delete, sender=Course)
def delete_course(sender, instance, **kwargs):
    for lesson in instance.lessons.all():
        lesson.delete()
    for assignment in instance.assignments.all():
        assignment.delete()


# Update teacher whenever a course is assigned to a teacher
@receiver(post_save, sender=Course)
def update_teacher(sender, instance, **kwargs):
    instance.teacher.teaching_courses.add(instance)

@receiver(post_delete, sender=Course)
def remove_teacher(sender, instance, **kwargs):
    if instance.teacher:
        instance.teacher.teaching_courses.remove(instance)
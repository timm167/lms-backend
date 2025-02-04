from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from core.models import Teacher, Student, Admin, Assignment, Lesson, Course, Enrollment

# Update enrollments whenever a student is added or removed from a course
@receiver(m2m_changed, sender=Course.students.through)
def update_enrollments(sender, instance, action, model, pk_set, **kwargs):
    if action == "post_add":
        # Add each student to their enrolled courses and create an enrollment entry
        for pk in pk_set:
            student = Student.objects.get(pk=pk)
            if instance not in student.enrolled_courses.all():  # Prevent duplicates
                student.enrolled_courses.add(instance)
                Enrollment.objects.get_or_create(course=instance, student=student)
    elif action == "post_remove":
        # Remove each student from their enrolled courses and delete the enrollment entry
        for pk in pk_set:
            student = Student.objects.get(pk=pk)
            student.enrolled_courses.remove(instance)
            Enrollment.objects.filter(course=instance, student=student).delete()
    elif action == "post_clear":
        # When students are cleared from the course, remove them from their enrolled courses
        for student in instance.students.all():
            student.enrolled_courses.remove(instance)
        # Delete all enrollment entries for this course
        Enrollment.objects.filter(course=instance).delete()



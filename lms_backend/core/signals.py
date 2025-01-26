from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from .models import Course, Enrollment, Teacher, Student, Admin


# Delete user when teacher, student, or admin is deleted
@receiver(post_delete, sender=Teacher)
def delete_teacher_user(sender, instance, **kwargs):
    instance.user.delete()

@receiver(post_delete, sender=Student)
def delete_student_user(sender, instance, **kwargs):
    instance.user.delete()

@receiver(post_delete, sender=Admin)
def delete_admin_user(sender, instance, **kwargs):
    instance.user.delete()


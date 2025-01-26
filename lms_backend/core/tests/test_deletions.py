from django.test import TestCase
from core.models import User, Student, Teacher, Admin

class UserDeletionTests(TestCase):

    def setUp(self):
        self.user_manager = User.objects

    def test_delete_teacher_deletes_user(self):
        teacher_user = self.user_manager.create(
            username='teacher', 
            password='password', 
            role='teacher',
            email='teacher@example.com'
        )
        self.assertTrue(User.objects.filter(username='teacher').exists())
        self.assertTrue(Teacher.objects.filter(user_id=teacher_user.id).exists())

        teacher_user.teacher.delete()
        self.assertFalse(User.objects.filter(username='teacher').exists())
        self.assertFalse(Teacher.objects.filter(user=teacher_user).exists())

    def test_delete_student_deletes_user(self):
        student_user = self.user_manager.create(
            username='student', 
            password='password', 
            role='student',
            email='student@example.com'
        )
        self.assertTrue(User.objects.filter(username='student').exists())
        self.assertTrue(Student.objects.filter(user=student_user).exists())

        student_user.student.delete()
        self.assertFalse(User.objects.filter(username='student').exists())
        self.assertFalse(Student.objects.filter(user=student_user).exists())

    def test_delete_admin_deletes_user(self):
        admin_user = self.user_manager.create(
            username='admin', 
            password='password', 
            role='admin',
            email='admin@example.com'
        )
        self.assertTrue(User.objects.filter(username='admin').exists())
        self.assertTrue(Admin.objects.filter(user=admin_user).exists())

        admin_user.admin.delete()
        self.assertFalse(User.objects.filter(username='admin').exists())
        self.assertFalse(Admin.objects.filter(user=admin_user).exists())
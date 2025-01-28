from django.test import TestCase
from lms_backend.core.models.models import User, Student, Teacher, Admin

class UserCreationTests(TestCase):

    def setUp(self):
        self.user_manager = User.objects

    def test_create_student_user_creates_student(self):
        student_user = self.user_manager.create_user(
            username='student', 
            password='password', 
            role='student',
            email='student@example.com'
        )
        print(student_user)
        self.assertIsInstance(student_user, User)
        self.assertTrue(Student.objects.filter(user=student_user).exists())
        self.assertFalse(Teacher.objects.filter(user=student_user).exists())
        self.assertFalse(Admin.objects.filter(user=student_user).exists())
        self.assertEqual(student_user.student.user, student_user)

    def test_create_teacher_user_creates_teacher(self):
        teacher_user = self.user_manager.create(
            username='teacher', 
            password='password', 
            role='teacher',
            email='teacher@example.com'
        )
        self.assertIsInstance(teacher_user, User)
        self.assertTrue(Teacher.objects.filter(user=teacher_user).exists())
        self.assertFalse(Student.objects.filter(user=teacher_user).exists())
        self.assertFalse(Admin.objects.filter(user=teacher_user).exists())
        self.assertEqual(teacher_user.teacher.user, teacher_user)


    def test_create_admin_user_creates_admin(self):
        admin_user = self.user_manager.create(
            username='admin', 
            password='password', 
            role='admin',
            email='admin@example.com'
        )
        self.assertIsInstance(admin_user, User)
        self.assertTrue(Admin.objects.filter(user=admin_user).exists())
        self.assertFalse(Student.objects.filter(user=admin_user).exists())
        self.assertFalse(Teacher.objects.filter(user=admin_user).exists())
        self.assertEqual(admin_user.admin.user, admin_user)


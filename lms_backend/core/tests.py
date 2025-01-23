from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Lesson, User


# Permission Tests
class PermissionTests(APITestCase):

    # Setup
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='admin', is_staff=True)
        self.teacher_user = User.objects.create_user(username='teacher', password='password', role='teacher')
        self.student_user = User.objects.create_user(username='student', password='password', role='student')

    # User Creation Permissions

    def test_admin_can_access_user_creation(self):
        self.client.login(username='admin', password='password')
        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_teacher_cannot_access_user_creation(self):
        self.client.login(username='teacher', password='password')
        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_access_user_creation(self):
        self.client.login(username='student', password='password')
        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # 


    # Lesson Creation Permissions

    def test_admin_can_access_lesson_creation(self):
        self.client.login(username='admin', password='password')
        url = reverse('lesson-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_can_access_lesson_creation(self):
        self.client.login(username='teacher', password='password')
        url = reverse('lesson-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_access_lesson_creation(self):
        self.client.login(username='student', password='password')
        url = reverse('lesson-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    # 


# View Tests
class LessonViewTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher', password='password', role='teacher')
        self.client.login(username='teacher', password='password')

    def test_create_lesson(self):
        url = reverse('lesson-list-create')
        data = {
            "title": "Sample Lesson",
            "description": "This is a test lesson."
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)


# Model Tests
class LessonModelTests(APITestCase):
    def test_lesson_creation(self):
        lesson = Lesson.objects.create(title="Test Lesson", description="Testing the lesson model.")
        self.assertEqual(str(lesson), "Test Lesson")

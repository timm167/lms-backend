from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Lesson, User


## ---------------------------------------------------- 
## Permission Tests 
## ---------------------------------------------------- 

# These tests only check permissions, not functionality.
# Methods in managers are not tested here.
# Delete method also covers update and partial update permissions as they have equivalent permissions.
class UserPermissionTests(APITestCase):

    # Setup

    def setUp(self):
        User.objects.all().delete()  
        self.admin_user = User.objects.create_user(
            username='admin', 
            password='password', 
            role='admin', 
            is_staff=True, 
            email='admin@example.com'
        )
        self.teacher_user = User.objects.create_user(
            username='teacher', 
            password='password', 
            role='teacher', 
            email='teacher@example.com'
        )
        self.student_user = User.objects.create_user(
            username='student', 
            password='password', 
            role='student', 
            email='student@example.com'
        )

    # User View Permissions

    def test_admin_can_access_user_view(self):
        self.client.login(username='admin', password='password')
        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_cannot_access_user_view(self):
        self.client.login(username='teacher', password='password')
        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_access_user_view(self):
        self.client.login(username='student', password='password')
        url = reverse('user-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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

    # User Deletion Permissions

    def test_admin_can_delete_user(self):
        self.client.login(username='admin', password='password')
        url = reverse('user-detail', args=[self.teacher_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_teacher_cannot_delete_user(self):
        self.client.login(username='teacher', password='password')
        url = reverse('user-detail', args=[self.student_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_delete_user(self):
        self.client.login(username='student', password='password')
        url = reverse('user-detail', args=[self.admin_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TeacherPermissionTests(APITestCase):

    # Setup
    def setUp(self):
        User.objects.all().delete()  
        self.admin_user = User.objects.create_user(
            username='admin', 
            password='password', 
            role='admin', 
            is_staff=True, 
            email='admin@example.com'
        )
        self.teacher_user = User.objects.create_user(
            username='teacher', 
            password='password', 
            role='teacher', 
            email='teacher@example.com'
        )
        self.student_user = User.objects.create_user(
            username='student', 
            password='password', 
            role='student', 
            email='student@example.com'
        )

    # Teacher View Permissions
    def test_admin_can_access_teacher_view(self):
        self.client.login(username='admin', password='password')
        url = reverse('teacher-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_cannot_access_teacher_view(self):
        self.client.login(username='teacher', password='password')
        url = reverse('teacher-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_access_teacher_view(self):
        self.client.login(username='student', password='password')
        url = reverse('teacher-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Teacher Creation Permissions

    def test_admin_can_access_teacher_creation(self):
        self.client.login(username='admin', password='password')
        url = reverse('teacher-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_cannot_access_teacher_creation(self):
        self.client.login(username='teacher', password='password')
        url = reverse('teacher-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_access_teacher_creation(self):
        self.client.login(username='student', password='password')
        url = reverse('teacher-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Teacher Deletion Permissions

    def test_admin_can_delete_teacher(self):
        self.client.login(username='admin', password='password')
        url = reverse('teacher-detail', args=[self.teacher_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_teacher_cannot_delete_teacher(self):
        self.client.login(username='teacher', password='password')
        url = reverse('teacher-detail', args=[self.teacher_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_delete_teacher(self):
        self.client.login(username='student', password='password')
        url = reverse('teacher-detail', args=[self.teacher_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StudentPermissionTests(APITestCase):

    # Setup
    def setUp(self):
        User.objects.all().delete()  
        self.admin_user = User.objects.create_user(
            username='admin', 
            password='password', 
            role='admin', 
            is_staff=True, 
            email='admin@example.com'
        )
        self.teacher_user = User.objects.create_user(
            username='teacher', 
            password='password', 
            role='teacher', 
            email='teacher@example.com'
        )
        self.student_user = User.objects.create_user(
            username='student', 
            password='password', 
            role='student', 
            email='student@example.com'
        )


    # Student View Permissions

    def test_admin_can_access_student_view(self):
        self.client.login(username='admin', password='password')
        url = reverse('student-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_cannot_access_student_view(self):
        self.client.login(username='teacher', password='password')
        url = reverse('student-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_access_student_view(self):
        self.client.login(username='student', password='password')
        url = reverse('student-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Student Creation Permissions

    def test_admin_can_access_student_creation(self):
        self.client.login(username='admin', password='password')
        url = reverse('student-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_cannot_access_student_creation(self):
        self.client.login(username='teacher', password='password')
        url = reverse('student-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_access_student_creation(self):
        self.client.login(username='student', password='password')
        url = reverse('student-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Student Deletion Permissions

    def test_admin_can_delete_student(self):
        self.client.login(username='admin', password='password')
        url = reverse('student-detail', args=[self.student_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_teacher_cannot_delete_student(self):
        self.client.login(username='teacher', password='password')
        url = reverse('student-detail', args=[self.student_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_delete_student(self):
        self.client.login(username='student', password='password')
        url = reverse('student-detail', args=[self.student_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
class CoursePermissionTests(APITestCase):

    # Setup
    def setUp(self):
        User.objects.all().delete()  
        self.admin_user = User.objects.create_user(
            username='admin', 
            password='password', 
            role='admin', 
            is_staff=True, 
            email='admin@example.com'
        )
        self.teacher_user = User.objects.create_user(
            username='teacher', 
            password='password', 
            role='teacher', 
            email='teacher@example.com'
        )
        self.student_user = User.objects.create_user(
            username='student', 
            password='password', 
            role='student', 
            email='student@example.com'
        )


    # Course View Permissions
    def test_admin_can_access_course_view(self):
        self.client.login(username='admin', password='password')
        url = reverse('course-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_can_access_course_view(self):
        self.client.login(username='teacher', password='password')
        url = reverse('course-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_access_course_view(self):
        self.client.login(username='student', password='password')
        url = reverse('course-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Course Creation Permissions

    def test_admin_can_access_course_creation(self):
        self.client.login(username='admin', password='password')
        url = reverse('course-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_can_access_course_creation(self):
        self.client.login(username='teacher', password='password')
        url = reverse('course-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_access_course_creation(self):
        self.client.login(username='student', password='password')
        url = reverse('course-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Course Deletion Permissions

    def test_admin_can_delete_course(self):
        self.client.login(username='admin', password='password')
        url = reverse('course-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_teacher_can_delete_course(self):
        self.client.login(username='teacher', password='password')
        url = reverse('course-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_student_cannot_delete_course(self):
        self.client.login(username='student', password='password')
        url = reverse('course-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LessonAssignmentPermissionTests(APITestCase):

    # Setup
    def setUp(self):
        User.objects.all().delete()  
        self.admin_user = User.objects.create_user(
            username='admin', 
            password='password', 
            role='admin', 
            is_staff=True, 
            email='admin@example.com'
        )
        self.teacher_user = User.objects.create_user(
            username='teacher', 
            password='password', 
            role='teacher', 
            email='teacher@example.com'
        )
        self.student_user = User.objects.create_user(
            username='student', 
            password='password', 
            role='student', 
            email='student@example.com'
        )


    # Lesson View Permissions

    def test_admin_can_access_lesson_view(self):
        self.client.login(username='admin', password='password')
        url = reverse('lesson-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_can_access_lesson_view(self):
        self.client.login(username='teacher', password='password')
        url = reverse('lesson-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_access_lesson_view(self):
        self.client.login(username='student', password='password')
        url = reverse('lesson-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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


    # Lesson Deletion Permissions

    def test_admin_can_delete_lesson(self):
        lesson = Lesson.objects.create(title='Test Lesson', content='Test Content', lesson_no=1)
        self.client.login(username='admin', password='password')
        url = reverse('lesson-detail', args=[lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_teacher_can_delete_lesson(self):
        lesson = Lesson.objects.create(title='Test Lesson', content='Test Content', lesson_no=1)
        self.client.login(username='teacher', password='password')
        url = reverse('lesson-detail', args=[lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_student_cannot_delete_lesson(self):
        lesson = Lesson.objects.create(title='Test Lesson', content='Test Content', lesson_no=1)
        self.client.login(username='student', password='password')
        url = reverse('lesson-detail', args=[lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AssignmentPermissionTests(APITestCase):

    # Setup
    def setUp(self):
        User.objects.all().delete()  
        self.admin_user = User.objects.create_user(
            username='admin', 
            password='password', 
            role='admin', 
            is_staff=True, 
            email='admin@example.com'
        )
        self.teacher_user = User.objects.create_user(
            username='teacher', 
            password='password', 
            role='teacher', 
            email='teacher@example.com'
        )
        self.student_user = User.objects.create_user(
            username='student', 
            password='password', 
            role='student', 
            email='student@example.com'
        )


    # Assignment View Permissions
    def test_admin_can_access_assignment_view(self):
        self.client.login(username='admin', password='password')
        url = reverse('assignment-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_can_access_assignment_view(self):
        self.client.login(username='teacher', password='password')
        url = reverse('assignment-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_access_assignment_view(self):
        self.client.login(username='student', password='password')
        url = reverse('assignment-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Assignment Creation Permissions

    def test_admin_can_access_assignment_creation(self):
        self.client.login(username='admin', password='password')
        url = reverse('assignment-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_can_access_assignment_creation(self):
        self.client.login(username='teacher', password='password')
        url = reverse('assignment-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_access_assignment_creation(self):
        self.client.login(username='student', password='password')
        url = reverse('assignment-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Assignment Deletion Permissions

    def test_admin_can_delete_assignment(self):
        lesson = Lesson.objects.create(title='Test Lesson', content='Test Content', lesson_no=1)
        self.client.login(username='admin', password='password')
        url = reverse('assignment-detail', args=[lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_teacher_can_delete_assignment(self):
        lesson = Lesson.objects.create(title='Test Lesson', content='Test Content', lesson_no=1)
        self.client.login(username='teacher', password='password')
        url = reverse('assignment-detail', args=[lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_student_cannot_delete_assignment(self):
        lesson = Lesson.objects.create(title='Test Lesson', content='Test Content', lesson_no=1)
        self.client.login(username='student', password='password')
        url = reverse('assignment-detail', args=[lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
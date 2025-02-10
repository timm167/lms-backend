# from django.urls import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status
# from core.models import User, Course, Teacher, Student, Lesson, Assignment, Enrollment
# from core.views.manager_views.course_manager_views import CourseManagerView
# from django.utils import timezone


# #------------------------------------------------------------#
# # Test as Teacher
# #------------------------------------------------------------#

# class CourseManagerViewTestsTeacher(APITestCase):

#     def setUp(self):
#         # Create a user and authenticate
#         self.user = User.objects.create_user(username='teacher', password='password', role='teacher', email='teacher@example.com')
#         self.client.force_authenticate(user=self.user)
        
#         # Create a teacher if it doesn't already exist
#         self.teacher, created = Teacher.objects.get_or_create(user=self.user)
        
#         # Create a course
#         self.course = Course.objects.create(title="Course 1", description="Description 1", teacher=self.teacher)
        
#         # URL for the CourseManagerView
#         self.url = reverse('course-manager')

#     def test_create_course(self):
#         data = {
#             'action': 'create_course',
#             'title': 'New Course',
#             'description': 'New Course Description',
#             'user_id': self.user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['message'], 'Course created successfully.')
#         self.assertTrue(Course.objects.filter(title='New Course').exists())

#     def test_delete_course(self):
#         data = {
#             'action': 'delete_course',
#             'course_id': self.course.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['error'], 'You do not have permission to perform this action.')

#     def test_add_and_delete_lesson(self):
#         # Add lesson
#         add_data = {
#             'action': 'add_lesson',
#             'course_id': self.course.id,
#             'title': 'New Lesson',
#             'content': 'Lesson Content',
#             'video_url': 'http://example.com/video'
#         }
#         add_response = self.client.post(self.url, add_data, format='json')
#         self.assertEqual(add_response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(add_response.data['message'], 'Lesson created successfully.')
#         self.assertTrue(self.course.lessons.filter(title='New Lesson').exists())
#         self.assertTrue(Lesson.objects.filter(title='New Lesson', course=self.course).exists())

#         # Get the created lesson
#         lesson = self.course.lessons.get(title='New Lesson')

#         # Delete lesson
#         delete_data = {
#             'action': 'delete_lesson',
#             'course_id': self.course.id,
#             'item_id': lesson.id
#         }
#         delete_response = self.client.post(self.url, delete_data, format='json')
#         self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(delete_response.data['message'], 'Lesson deleted successfully.')

#     def test_add_and_delete_assignment(self):
#         # Add assignment
#         add_data = {
#             'action': 'add_assignment',
#             'course_id': self.course.id,
#             'title': 'New Assignment',
#             'description': 'Assignment Description',
#             'due_date': timezone.make_aware(timezone.datetime(2023, 12, 31)),
#             'max_score': 100,
#             'pass_score': 50
#         }
#         add_response = self.client.post(self.url, add_data, format='json')
#         self.assertEqual(add_response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(add_response.data['message'], 'Assignment created successfully.')
#         self.assertTrue(self.course.assignments.filter(title='New Assignment').exists())
#         self.assertTrue(Assignment.objects.filter(title='New Assignment', course=self.course).exists())

#         # Get the created assignment
#         assignment = self.course.assignments.get(title='New Assignment')

#         # Delete assignment
#         delete_data = {
#             'action': 'delete_assignment',
#             'course_id': self.course.id,
#             'item_id': assignment.id
#         }
#         delete_response = self.client.post(self.url, delete_data, format='json')
#         self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(delete_response.data['message'], 'Assignment deleted successfully.')

#     def test_enroll_student(self):
#         # Create a student
#         student_user = User.objects.create_user(username='student', password='password', role='student', email='student@example.com')
#         student = Student.objects.get(user=student_user)
#         data = {
#             'action': 'enroll_student',
#             'course_id': self.course.id,
#             'user_id': student_user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['error'], 'You do not have permission to perform this action.')

#     def test_unenroll_student(self):
#         # Create a student and enroll them first
#         student_user = User.objects.create_user(username='student', password='password', role='student', email='student@example.com')
#         student = Student.objects.get(user=student_user)
#         self.course.students.add(student)
#         data = {
#             'action': 'unenroll_student',
#             'course_id': self.course.id,
#             'user_id': student_user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['error'], 'You do not have permission to perform this action.')

#     def test_add_teacher(self):
#         # Create another teacher
#         new_teacher_user = User.objects.create_user(username='new_teacher', password='password', role='teacher', email='new_teacher@example.com')
#         data = {
#             'action': 'add_teacher',
#             'course_id': self.course.id,
#             'user_id': new_teacher_user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['error'], 'You do not have permission to perform this action.')

#     def test_remove_teacher(self):
#         data = {
#             'action': 'remove_teacher',
#             'course_id': self.course.id,
#             'user_id': self.teacher.user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['error'], 'You do not have permission to perform this action.')




# #------------------------------------------------------------#
# # Test as Admin
# #------------------------------------------------------------#

# class CourseManagerViewTestsAdmin(APITestCase):

#     def setUp(self):
#         # Create an admin user and authenticate
#         self.user = User.objects.create_user(username='admin', password='password', role='admin', email='admin@example.com')
#         self.client.force_authenticate(user=self.user)
        
#         # Create a teacher user for the course
#         self.teacher_user = User.objects.create_user(username='teacher', password='password', role='teacher', email='teacher@example.com')
#         self.teacher, created = Teacher.objects.get_or_create(user=self.teacher_user)
        
#         # Create a course
#         self.course = Course.objects.create(title="Course 1", description="Description 1", teacher=self.teacher)
        
#         # URL for the CourseManagerView
#         self.url = reverse('course-manager')

#     def test_create_course(self):
#         data = {
#             'action': 'create_course',
#             'title': 'New Course',
#             'description': 'New Course Description',
#             'user_id': self.teacher_user.id  # Assign the course to the teacher
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['message'], 'Course created successfully.')
#         self.assertTrue(Course.objects.filter(title='New Course').exists())

#     def test_delete_course(self):
#         data = {
#             'action': 'delete_course',
#             'course_id': self.course.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Course deleted successfully.')

#     def test_add_and_delete_lesson(self):
#         # Add lesson
#         add_data = {
#             'action': 'add_lesson',
#             'course_id': self.course.id,
#             'title': 'New Lesson',
#             'content': 'Lesson Content',
#             'video_url': 'http://example.com/video'
#         }
#         add_response = self.client.post(self.url, add_data, format='json')
#         self.assertEqual(add_response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(add_response.data['message'], 'Lesson created successfully.')
#         self.assertTrue(self.course.lessons.filter(title='New Lesson').exists())
#         self.assertTrue(Lesson.objects.filter(title='New Lesson', course=self.course).exists())

#         # Get the created lesson
#         lesson = self.course.lessons.get(title='New Lesson')

#         # Delete lesson
#         delete_data = {
#             'action': 'delete_lesson',
#             'course_id': self.course.id,
#             'item_id': lesson.id
#         }
#         delete_response = self.client.post(self.url, delete_data, format='json')
#         self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(delete_response.data['message'], 'Lesson deleted successfully.')
        
#     def test_add_and_delete_assignment(self):
#         # Add assignment
#         add_data = {
#             'action': 'add_assignment',
#             'course_id': self.course.id,
#             'title': 'New Assignment',
#             'description': 'Assignment Description',
#             'due_date': timezone.make_aware(timezone.datetime(2023, 12, 31)),
#             'max_score': 100,
#             'pass_score': 50
#         }
#         add_response = self.client.post(self.url, add_data, format='json')
#         self.assertEqual(add_response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(add_response.data['message'], 'Assignment created successfully.')
#         self.assertTrue(self.course.assignments.filter(title='New Assignment').exists())
#         self.assertTrue(Assignment.objects.filter(title='New Assignment', course=self.course).exists())

#         # Get the created assignment
#         assignment = self.course.assignments.get(title='New Assignment')

#         # Delete assignment
#         delete_data = {
#             'action': 'delete_assignment',
#             'course_id': self.course.id,
#             'item_id': assignment.id
#         }
#         delete_response = self.client.post(self.url, delete_data, format='json')
#         self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(delete_response.data['message'], 'Assignment deleted successfully.')
    
#     def test_enroll_student(self):
#         # Create a student
#         student_user = User.objects.create_user(username='student', password='password', role='student', email='student@example.com')
#         student = Student.objects.get(user=student_user)
#         data = {
#             'action': 'enroll_student',
#             'course_id': self.course.id,
#             'user_id': student_user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Student enrolled successfully.')
#         # Check enrollment works fully
#         self.assertTrue(self.course.students.filter(user=student_user).exists())
#         student = Student.objects.get(user=student_user)
#         self.assertTrue(student.enrolled_courses.filter(id=self.course.id).exists())
#         self.assertTrue(Enrollment.objects.filter(course=self.course, student=student).exists())


#     def test_unenroll_student(self):
#         # Create a student and enroll them first
#         student_user = User.objects.create_user(username='student', password='password', role='student', email='student@example.com')
#         student = Student.objects.get(user=student_user)
#         self.course.students.add(student)
#         data = {
#             'action': 'unenroll_student',
#             'course_id': self.course.id,
#             'user_id': student_user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Student unenrolled successfully.')
#         # Check unenrollment works fully
#         self.assertFalse(self.course.students.filter(user=student_user).exists())
#         student = Student.objects.get(user=student_user)
#         self.assertFalse(student.enrolled_courses.filter(id=self.course.id).exists())
#         self.assertFalse(Enrollment.objects.filter(course=self.course, student=student).exists())

#     def test_add_teacher(self):
#         # Create another teacher
#         new_teacher_user = User.objects.create_user(username='new_teacher', password='password', role='teacher', email='new_teacher@example.com')
#         new_teacher = Teacher.objects.get(user=new_teacher_user)
#         data = {
#             'action': 'add_teacher',
#             'course_id': self.course.id,
#             'user_id': new_teacher_user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Teacher added successfully.')
#         self.course.refresh_from_db()
#         self.assertTrue(self.course.teacher == new_teacher)
#         self.assertTrue(new_teacher.teaching_courses.filter(id=self.course.id).exists())

#     def test_remove_teacher(self):
#         data = {
#             'action': 'remove_teacher',
#             'course_id': self.course.id,
#             'user_id': self.teacher.user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Teacher removed successfully.')
#         self.course.refresh_from_db()
#         teacher = Teacher.objects.get(user=self.teacher.user)
#         self.assertFalse(self.course.teacher == self.teacher)
#         self.assertFalse(teacher.teaching_courses.filter(id=self.course.id).exists())



# #------------------------------------------------------------#
# # Test as Student
# #------------------------------------------------------------#

# class CourseManagerViewTestsStudent(APITestCase):

#     def setUp(self):
#         # Create a student user and authenticate
#         self.user = User.objects.create_user(username='student', password='password', role='student', email='student@example.com')
#         self.client.force_authenticate(user=self.user)
        
#         # Create a teacher user for the course
#         self.teacher_user = User.objects.create_user(username='teacher', password='password', role='teacher', email='teacher@example.com')
#         self.teacher, created = Teacher.objects.get_or_create(user=self.teacher_user)
        
#         # Create a course
#         self.course = Course.objects.create(title="Course 1", description="Description 1", teacher=self.teacher)
        
#         # URL for the CourseManagerView
#         self.url = reverse('course-manager')

#     # Enroll and unenroll self

#     def test_enroll_self(self):
#         data = {
#             'action': 'enroll_student',
#             'course_id': self.course.id,
#             'user_id': self.user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Student enrolled successfully.')
        
#         # Check that the student is enrolled in the course
#         self.assertTrue(self.course.students.filter(user=self.user).exists())
#         student = Student.objects.get(user=self.user)
#         self.assertTrue(student.enrolled_courses.filter(id=self.course.id).exists())
#         self.assertTrue(Enrollment.objects.filter(course=self.course, student=student).exists())

#     def test_unenroll_self(self):
#         # Unenroll self
#         student = Student.objects.get(user=self.user)
#         self.course.students.add(student)
        
#         data = {
#             'action': 'unenroll_student',
#             'course_id': self.course.id,
#             'user_id': self.user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Student unenrolled successfully.')
        
#         # Check that the student is no longer enrolled in the course
#         self.assertFalse(self.course.students.filter(user=self.user).exists())
#         self.assertFalse(student.enrolled_courses.filter(id=self.course.id).exists())
#         self.assertFalse(Enrollment.objects.filter(course=self.course, student=student).exists())

#     # Attempt to enroll and unenroll another student
    
#     def test_enroll_another_student(self):
#         # Create another student
#         another_student_user = User.objects.create_user(username='another_student', password='password', role='student', email='another_student@example.com')
#         data = {
#             'action': 'enroll_student',
#             'course_id': self.course.id,
#             'user_id': another_student_user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['error'], 'You do not have permission to perform this action.')

#     def test_unenroll_another_student(self):
#         # Create another student and enroll them first
#         another_student_user = User.objects.create_user(username='another_student', password='password', role='student', email='another_student@example.com')
#         another_student = Student.objects.get(user=another_student_user)
#         self.course.students.add(another_student)
#         data = {
#             'action': 'unenroll_student',
#             'course_id': self.course.id,
#             'user_id': another_student_user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['error'], 'You do not have permission to perform this action.')


#     def test_create_course(self):
#         data = {
#             'action': 'create_course',
#             'title': 'New Course',
#             'description': 'New Course Description',
#             'user_id': self.teacher_user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['error'], 'You do not have permission to perform this action.')

#     def test_delete_course(self):
#         data = {
#             'action': 'delete_course',
#             'course_id': self.course.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['error'], 'You do not have permission to perform this action.')

#     def test_add_and_delete_lesson(self):
#         # Add lesson
#         add_data = {
#             'action': 'add_lesson',
#             'course_id': self.course.id,
#             'title': 'New Lesson',
#             'content': 'Lesson Content',
#             'video_url': 'http://example.com/video'
#         }
#         add_response = self.client.post(self.url, add_data, format='json')
#         self.assertEqual(add_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(add_response.data['error'], 'You do not have permission to perform this action.')

#         # Attempt to delete lesson (should not be able to add, so no lesson to delete)
#         delete_data = {
#             'action': 'delete_lesson',
#             'course_id': self.course.id,
#             'item_id': 1  # Assuming an ID that doesn't exist
#         }
#         delete_response = self.client.post(self.url, delete_data, format='json')
#         self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(delete_response.data['error'], 'You do not have permission to perform this action.')

#     def test_add_and_delete_assignment(self):
#         # Add assignment
#         add_data = {
#             'action': 'add_assignment',
#             'course_id': self.course.id,
#             'title': 'New Assignment',
#             'description': 'Assignment Description',
#             'due_date': timezone.make_aware(timezone.datetime(2023, 12, 31)),
#             'max_score': 100,
#             'pass_score': 50
#         }
#         add_response = self.client.post(self.url, add_data, format='json')
#         self.assertEqual(add_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(add_response.data['error'], 'You do not have permission to perform this action.')

#         # Attempt to delete assignment (should not be able to add, so no assignment to delete)
#         delete_data = {
#             'action': 'delete_assignment',
#             'course_id': self.course.id,
#             'item_id': 1 
#         }
#         delete_response = self.client.post(self.url, delete_data, format='json')
#         self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(delete_response.data['error'], 'You do not have permission to perform this action.')

#     def test_add_teacher(self):
#         # Create another teacher
#         new_teacher_user = User.objects.create_user(username='new_teacher', password='password', role='teacher', email='new_teacher@example.com')
#         data = {
#             'action': 'add_teacher',
#             'course_id': self.course.id,
#             'user_id': new_teacher_user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['error'], 'You do not have permission to perform this action.')

#     def test_remove_teacher(self):
#         data = {
#             'action': 'remove_teacher',
#             'course_id': self.course.id,
#             'user_id': self.teacher.user.id
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(response.data['error'], 'You do not have permission to perform this action.')

    
from django.test import TestCase
from django.test import TestCase
from lms_backend.core.models.models import Course, Lesson

class LessonCreationTestCase(TestCase):

    def setUp(self):
        # Create two course instances
        self.course_instance_1 = Course.objects.create(title="Course 1", description="Description 1")
        self.course_instance_2 = Course.objects.create(title="Course 2", description="Description 2")

    def test_create_lesson(self):
        # Create a lesson for course_instance_1
        lesson_data = {
            'course': self.course_instance_1,
            'title': "Lesson Title",
            'content': "Lesson Content",
            'lesson_no': 1,
            'video_url': "http://example.com/video"
        }
        Lesson.objects.create_lesson(**lesson_data)
        self.assertTrue(Lesson.objects.filter(title="Lesson Title").exists())

    def test_lesson_creation(self):
        # Create a lesson for course_instance_1
        lesson_data = {
            'course': self.course_instance_1,
            'title': "Lesson Title",
            'content': "Lesson Content",
            'lesson_no': 1,
            'video_url': "http://example.com/video"
        }
        lesson_instance = Lesson.objects.create_lesson(**lesson_data)
        lessons_in_course_1 = Course.objects.get(id=self.course_instance_1.id).lessons.all()
        self.assertTrue(lesson_instance in lessons_in_course_1)

        lessons_in_course_2 = Course.objects.get(id=self.course_instance_2.id).lessons.all()
        self.assertFalse(lesson_instance in lessons_in_course_2)
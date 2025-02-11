from faker import Faker
from core.models import User, Course, Teacher, Student, Lesson, Assignment
from rest_framework.response import Response
from rest_framework import status
import random
from rest_framework.views import APIView
from django.utils import timezone
from datetime import datetime

class RefreshData(APIView):
    def post(self, request):
        generate_users()
        generate_courses()
        generate_enrollments()
        return Response({'message': 'Data generated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request):
        users_to_delete = User.objects.exclude(is_superuser=True)
        count, _ = users_to_delete.delete() 
        objects_to_delete = Course.objects.all()
        count, _ = objects_to_delete.delete()
        return Response({'message': 'Data deleted successfully'}, status=status.HTTP_200_OK)


fake = Faker()

def generate_courses():
    teachers = Teacher.objects.all()
    course_data = [
        ("Math", "Fundamentals of mathematics and problem-solving techniques."),
        ("Science", "Introduction to scientific principles and experiments."),
        ("History", "Study of historical events and civilizations."),
        ("English", "Understanding literature, grammar, and writing skills."),
    ]
    
    for title, description in course_data:
        teacher = random.choice(teachers) if teachers else None
        course = Course.objects.create_course(title=title, description=description, teacher=teacher)
        generate_lessons_for_course(course)
        generate_assignments_for_course(course)

def generate_users():
    predefined_users = ['student', 'teacher', 'admin']
    
    # Loop through and create each user individually
    for role in predefined_users:
        if not User.objects.filter(username=role).exists():
            User.objects.create_user(
                username=role,
                first_name=role.capitalize(),
                last_name="User",
                email=f"{role}@example.com",
                password=role,
                role=role
            )
    
    # Create 16 students with random names
    for _ in range(16):
        first_name = fake.first_name()
        last_name = fake.last_name()
        User.objects.create_user(
            username=f"{first_name.lower()}{last_name.lower()}",
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name.lower()}.{last_name.lower()}@example.com",
            password="password",
            role="student"
        )
    
    # Create 4 teachers with random names
    for _ in range(4):
        first_name = fake.first_name()
        last_name = fake.last_name()
        User.objects.create_user(
            username=f"{first_name.lower()}{last_name.lower()}",
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name.lower()}.{last_name.lower()}@example.com",
            password="password",
            role="teacher"
        )



def generate_enrollments():
    students = Student.objects.all()
    courses = Course.objects.all()
    
    for student in students:
        for course in random.sample(list(courses), min(len(courses), 2)):
            course.students.add(student)
            print(f"Student '{student.user.username}' enrolled in course: {course.title}")

def generate_lessons_for_course(course):
    lesson_mapping = {
        "Math": ["Algebra", "Geometry", "Calculus"],
        "Science": ["Physics Basics", "Chemistry Fundamentals", "Biology Overview"],
        "History": ["Ancient Civilizations", "Medieval Times", "Modern History"],
        "English": ["Grammar Essentials", "Literary Analysis", "Creative Writing"],
    }
    
    lessons = lesson_mapping.get(course.title, ["General Introduction", "Main Concepts", "Advanced Topics"])
    
    for index, title in enumerate(lessons, start=1):
        Lesson.objects.create(
            course=course,
            title=title,
            content=f"This is a lesson on {title} in the {course.title} course.",
            video_url="http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
        )
        print(f"Lesson '{title}' created for course: {course.title}")

def generate_assignments_for_course(course):
    assignment_titles = ["Quiz 1", "Midterm Project", "Final Exam"]
    
    for title in assignment_titles:
        due_date = timezone.make_aware(datetime.combine(fake.date_this_year(), datetime.min.time()))
        Assignment.objects.create(
            course=course,
            title=title,
            description=f"{title} for the {course.title} course.",
            due_date=due_date,
            max_score=100,
            pass_score=50
        )
        print(f"Assignment '{title}' created for course: {course.title}")

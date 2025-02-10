from faker import Faker
from core.models import User, Course, Teacher, Student, Lesson, Assignment
from rest_framework.response import Response
from rest_framework import status
import random
from rest_framework.views import APIView

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
        ("Computer Science", "Basics of programming and computational thinking."),
        ("Art", "Exploration of visual arts and creative expression."),
        ("Music", "Study of musical theory and practice."),
        ("Physical Education", "Development of physical fitness and sports skills."),
        ("Biology", "Examination of living organisms and life processes."),
        ("Chemistry", "Understanding chemical reactions and properties of matter."),
        ("Physics", "Study of the laws of nature and physical phenomena."),
        ("Geography", "Exploration of Earth's landscapes and environments."),
        ("Economics", "Introduction to economic principles and systems."),
        ("Philosophy", "Examination of fundamental questions about existence and knowledge."),
        ("Psychology", "Study of human behavior and mental processes.")
    ]
    
    for title, description in course_data:
        teacher = random.choice(teachers) if teachers else None
        course = Course.objects.create_course(title=title, description=description, teacher=teacher)
        generate_lessons_for_course(course)
        generate_assignments_for_course(course)

def generate_users():
    predefined_users = ['student', 'teacher', 'admin']
    
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
    
    for _ in range(5):
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
    
    for _ in range(2):
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
        "Computer Science": ["Programming Basics", "Data Structures", "Algorithms"]
    }
    
    lessons = lesson_mapping.get(course.title, ["General Introduction", "Main Concepts", "Advanced Topics"])
    
    for index, title in enumerate(lessons, start=1):
        Lesson.objects.create(
            course=course,
            title=title,
            content=f"This is a lesson on {title} in the {course.title} course.",
            video_url=f"https://example.com/{course.title.lower()}_{title.lower().replace(' ', '_')}"
        )
        print(f"Lesson '{title}' created for course: {course.title}")

def generate_assignments_for_course(course):
    assignment_titles = ["Quiz 1", "Midterm Project", "Final Exam"]
    
    for title in assignment_titles:
        Assignment.objects.create(
            course=course,
            title=title,
            description=f"{title} for the {course.title} course.",
            due_date=fake.date_this_year(),
            max_score=100,
            pass_score=50
        )
        print(f"Assignment '{title}' created for course: {course.title}")

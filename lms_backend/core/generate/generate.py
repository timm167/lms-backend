from faker import Faker
from core.models import User, Course, Teacher, Student, Lesson, Assignment
from rest_framework.response import Response
from rest_framework import status
import random

def delete_all_except_superusers(self):
    users_to_delete = User.objects.exclude(is_superuser=True)
    count, _ = users_to_delete.delete() 
    print(f"Deleted {count} users, superusers remain.")
    objects_to_delete = Course.objects.all()
    count, _ = objects_to_delete.delete()
    print(f"Deleted {count} courses.")
    return Response({'message': 'Data deleted successfully'}, status=status.HTTP_200_OK)

def generate_data(self):
    generate_users()
    generate_courses()
    return Response({'message': 'Data generated successfully'}, status=status.HTTP_201_CREATED)


fake = Faker()

def generate_courses():
    # Fetch existing teachers, students, lessons, and assignments to link them
    teachers = Teacher.objects.all()
    students = Student.objects.all()

    for _ in range(20):  
        instructor = random.choice(teachers) if teachers else None

        course = Course.objects.create(
            title=fake.sentence(nb_words=5),
            description=fake.text(max_nb_chars=300),
            instructor=instructor
        )
            # Generate lessons for this course
        generate_lessons_for_course(course)

        # Generate assignments for this course
        generate_assignments_for_course(course)

def generate_users():
    for _ in range(100):  # Create 100 fake users
        role = fake.random_element(elements=('student', 'teacher', 'admin'))

        User.objects.create_user(
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password=fake.password(),
            role=role
        )


def generate_lessons_for_course(course, num_lessons=3):
    for _ in range(num_lessons):
        lesson = Lesson.objects.create(
            course=course,
            title=fake.sentence(nb_words=5),
            content=fake.text(max_nb_chars=500),
            lesson_no=random.randint(1, 10),  
            video_url=fake.url()  
        )
        print(f"Lesson '{lesson.title}' created for course: {course.title}")

def generate_assignments_for_course(course, num_assignments=3):
    for _ in range(num_assignments):
        assignment = Assignment.objects.create(
            course=course,
            title=fake.sentence(nb_words=5),
            description=fake.text(max_nb_chars=300),
            due_date=fake.date_this_year(),  
            max_score=random.randint(50, 100),  
            pass_score=random.randint(30, 60) 
        )
        print(f"Assignment '{assignment.title}' created for course: {course.title}")

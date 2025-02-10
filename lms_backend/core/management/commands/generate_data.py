from django.core.management.base import BaseCommand
from core.generate import generate_users, generate_courses, generate_enrollments

class Command(BaseCommand):
    help = 'Generate users, courses, and enrollments'

    def handle(self, *args, **kwargs):
        generate_users()
        generate_courses()
        generate_enrollments()
        self.stdout.write(self.style.SUCCESS('Data generated successfully'))
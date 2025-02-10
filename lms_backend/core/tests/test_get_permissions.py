from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Lesson, User, Course, Teacher, Enrollment, Student
from django.utils import timezone
from rest_framework.authtoken.models import Token


## This should test API testCases for all the get permissions
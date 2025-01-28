from .accounts import MyLoginView, MySignupView
from .users import UserListCreateView, UserDetailView

# Create unified views here. 

# Add signals to update enrollments dynamically!!!!

# Includes the following views:
# TeacherView
# StudentView
# AdminView
# CourseView
# UserView
# LessonByCourseView
# AssignmentByCourseView
# EnrollmentsView

# Once I have these views, expose methods to the frontend to interact with them.
# This will define my user facing data model.
# This should take about a day to complete.
# Then I can sort the frontend out. (3-4 days)
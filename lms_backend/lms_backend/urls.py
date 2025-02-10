from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from core.views import (
    LoginView, 
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserTypeView,
    UserDetailView,
    StudentDetailView,
    TeacherDetailView,
    AdminDetailView,
    StudentListView,
    TeacherListView,
    AdminListView,
    CourseListView,
    CourseDetailView,
    BrowseCoursesView,
    LessonDetailView,
    AssignmentDetailView,
    EnrollmentListView,
    EnrollmentDetailView,
    CourseManagerView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from core.generate import RefreshData
from django.http import HttpResponse

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # API authentication
    path('token/', obtain_auth_token, name='api_token_auth'),

    # Generate data
    path('data/refresh/', RefreshData.as_view(), name='generate-data'),

    path('base-url/', lambda request: HttpResponse("Base URL is correct"), name='base-url-check'),



    # Swagger UI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Accounts
    path('accounts/login/',LoginView.as_view(), name='login'),
    path('accounts/signup/', UserCreateView.as_view(), name='signup'),

    # User Manager
    path('users/create/',UserCreateView.as_view(), name='create-user'),
    path('users/delete/',UserDeleteView.as_view(), name='delete-user'),
    path('user/type/', UserTypeView.as_view(), name='user-type'),

    # Course Manager
    path('course-manager/', CourseManagerView.as_view(), name='course-manager'),

    # Users
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Students
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),

    # Teachers
    path('teachers/', TeacherListView.as_view(), name='teacher-list'),
    path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),

    # Admins
    path('admins/', AdminListView.as_view(), name='admin-list'),
    path('admins/<int:pk>/', AdminDetailView.as_view(), name='admin-detail'),

    # Courses
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/browse/', BrowseCoursesView.as_view(), name='browse-courses'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    # Lessons
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),

    # Assignments
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),

    # Enrollments
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
]
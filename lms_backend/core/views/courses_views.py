from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from core.models import Course, Lesson, Assignment
from core.serializers import CourseSerializer, LessonSerializer, AssignmentSerializer, BrowseCourseSerializer
from .permissions.teachers_permissions import IsSelfTeacherOrAdmin

# Courses
class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsSelfTeacherOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(teacher=user.teacher)

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class BrowseCoursesView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = BrowseCourseSerializer
    permission_classes = [IsAuthenticated]
#------------------------------------------------------------#
# Lessons
#------------------------------------------------------------#

class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


#------------------------------------------------------------#
# Assignments
#------------------------------------------------------------#

class AssignmentDetailView(generics.RetrieveAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

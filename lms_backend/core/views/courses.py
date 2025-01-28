from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from core.models import Course, Lesson, Assignment
from core.serializers import CourseSerializer, LessonSerializer, AssignmentSerializer
from .permissions import IsSelfTeacherOrAdmin

# Courses
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsSelfTeacherOrAdmin]

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [IsSelfTeacherOrAdmin()]
        return [IsAuthenticated()]


#------------------------------------------------------------#
# Lessons
#------------------------------------------------------------#

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsSelfTeacherOrAdmin]

    def perform_create(self, serializer):
        print("creating lesson")
        course = Course.objects.get(id=self.request.data.get('course_id'))
        Lesson.objects.create_lesson(
            course=course,
            title=self.request.data.get('title'),
            content=self.request.data.get('content'),
            lesson_no=self.request.data.get('lesson_no'),
            video_url=self.request.data.get('video_url')
        )

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [IsSelfTeacherOrAdmin()]
        return [IsAuthenticated()]


#------------------------------------------------------------#
# Assignments
#------------------------------------------------------------#

class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsSelfTeacherOrAdmin]

    

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [IsSelfTeacherOrAdmin()]
        return [IsAuthenticated()]

from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from core.models import Enrollment
from core.serializers import EnrollmentSerializer
from .permissions import IsStudentOrAdmin, IsStudentOrTeacherOrAdmin

#------------------------------------------------------------#
# Enrollments
#------------------------------------------------------------#

class EnrollmentListCreateView(generics.ListCreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudentOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.all()
        elif user.role == 'teacher':
            return Enrollment.objects.filter(course__instructor=user.teacher)
        return Enrollment.objects.filter(student__user=user)

    def perform_create(self, serializer):
        if self.request.user.role == 'teacher':
            self.permission_denied(self.request, message="Only students and admins can create enrollments.")
        elif self.request.user.role == 'student':
            student = serializer.validated_data['student']
            if student.user == self.request.user:
                serializer.save(student=self.request.user.student)
        elif self.request.user.is_staff:
            serializer.save()

class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_permissions(self):
        if self.request.method in [ 'PUT', 'PATCH']:
            return [IsAdminUser()]
        if self.request.method in ['DELETE']:
            return [IsStudentOrAdmin()]
        return [IsStudentOrTeacherOrAdmin()]

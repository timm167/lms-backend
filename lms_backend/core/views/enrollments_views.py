from rest_framework import generics
from core.models import Enrollment
from core.serializers import EnrollmentSerializer
from .permissions.students_permissions import IsSelfStudentOrAdmin

#------------------------------------------------------------#
# Enrollments
#------------------------------------------------------------#

class EnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsSelfStudentOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.all()
        return Enrollment.objects.filter(student__user=user)
    
class EnrollmentDetailView(generics.RetrieveAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsSelfStudentOrAdmin]
    
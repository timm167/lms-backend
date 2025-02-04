from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import User

def validate_user_data(request, username, password, email, role):
    if not username or not password or not role or not email:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    if role != 'student':
        if not request.user or not request.user.is_authenticated or not request.user.is_staff:
            return Response({'error': 'Only admins can add non-student users'}, status=status.HTTP_403_FORBIDDEN)
    
    if not request.user or not request.user.is_authenticated:
        return 'signup'

    return 'create'
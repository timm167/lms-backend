from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import User
from django.contrib.auth import login, authenticate

# Login requires no authentication to avoid loop.
class MyLoginView(APIView):
    authentication_classes = []  
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        print("user:", user)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return Response({'message': 'Login successful',
                             "token": token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Permission Error'}, status=status.HTTP_401_UNAUTHORIZED)

## This set up lets people pick their own role. I will need to add a check to e
class MySignupView(APIView):
    authentication_classes = []  
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')


        if not username or not password or not role or not email:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        if role not in ['student', 'teacher', 'admin']: # Remove teacher and admin later.
            return Response({'error': 'Only admins can add that user type'}, status=status.HTTP_400_BAD_REQUEST)
        
        if first_name is None:
            first_name = 'user:'
            last_name = username

        user = User.objects.create_user(username=username, password=password, role=role, email=email, first_name=first_name, last_name=last_name)
        if user is not None:
            
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return Response({'message': 'Signup successful',
                             "token": token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Permission Error'}, status=status.HTTP_401_UNAUTHORIZED)
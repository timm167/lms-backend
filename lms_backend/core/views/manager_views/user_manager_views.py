from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import User
from django.contrib.auth import login
from ..permissions.user_validation import validate_user_data
from rest_framework.permissions import IsAuthenticated

# Signup view for users. Create view for admins to create users.
class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')
        email = request.data.get('email')
        first_name = request.data.get('first_name', 'New')
        last_name = request.data.get('last_name', 'User')

        response = validate_user_data(request, username, password, email, role)

        if response == 'create':
            print("Creating user")
            user = User.objects.create_user(username=username, password=password, role=role, email=email, first_name=first_name, last_name=last_name)
            return Response({'message': 'User created successfully', "user_id": user.id}, status=status.HTTP_201_CREATED)

        if response == 'signup':
            print("Signing up user")
            user = User.objects.create_user(username=username, password=password, role=role, email=email, first_name=first_name, last_name=last_name)
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message': 'Signup successful', "token": token.key}, status=status.HTTP_201_CREATED)

        return response
    
class UserDeleteView(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class UserTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_type = user.role
        return Response({"user_type": user_type}, status=status.HTTP_200_OK)
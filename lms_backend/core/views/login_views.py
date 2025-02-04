from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, authenticate


# Login requires no authentication to avoid loop.
class LoginView(APIView):
    authentication_classes = []  
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return Response({'message': 'Login successful',
                             "token": token.key,
                             "user_type": user.role}, status=status.HTTP_200_OK)
        return Response({'error': 'Permission Error'}, status=status.HTTP_401_UNAUTHORIZED)


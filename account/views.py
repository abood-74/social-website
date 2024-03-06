from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.password_validation import validate_password
from .serializers import LoginSerializer, RegisterSerializer
from .models import CustomUser

class RegisterView(APIView):
        
        def post(self, request):
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                print(serializer.validated_data)
                user = CustomUser.objects.create_user(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password']
                )
                user.save()
                return Response({'message': 'User created successfully'})
            
            
            return Response(serializer.errors, status=400)

class LoginView(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                login(request, user)
                return Response({'message': 'You have been logged in'})
            return Response({'message': 'Invalid credentials'}, status=401)
        
        return Response(serializer.errors, status=400)
            
        

class LogoutView(APIView):
    
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'You have been logged out'})
        
        return Response({'message': 'You are not logged in'}, status=400)
    


class PasswordChangeView(APIView): 
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if request.user.is_authenticated:
            
            try:
                validate_password(request.data['password'])
                request.user.set_password(request.data['password'])
                request.user.save()
                return Response({'message': 'Password changed successfully'})
            
            except Exception as e:
                return Response({'message': e.messages}, status=400)
            
        
        return Response({'message': 'You are not logged in'}, status=400)


class DashBoardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'message': f'Welcome to "{request.user.username}" the dashboard'})
        

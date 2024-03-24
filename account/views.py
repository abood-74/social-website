from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
#local imports
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer, EditUserSerializer

class RegisterView(APIView):
        
        def post(self, request):
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            
            
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status= status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status= status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        

class LogoutView(APIView):
    
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'You have been logged out'}, status = status.HTTP_200_OK)
        
        return Response({'message': 'You are not logged in'}, status= status.HTTP_400_BAD_REQUEST)
    


class PasswordChangeView(APIView): 
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if request.user.is_authenticated:
            
            try:
                validate_password(request.data['password'])
                request.user.set_password(request.data['password'])
                request.user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({'message': e.messages}, status=status.HTTP_400_BAD_REQUEST)
            
        

class UserEditView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'username':request.user.username, 'email': request.user.email, 'first_name': request.user.first_name})
    
    
    def put(self, request):
        serializer = UserSerializer(instance=request.user,data=request.data)
        if serializer.is_valid():     
            serializer.save()
            return Response({'message': 'User updated successfully'}, status=status.HTTP_201_CREATED) 
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = EditUserSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        

class DashBoardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'message': f'Welcome to "{request.user.username}" the dashboard'})
        

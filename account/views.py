from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer
from django.contrib.auth import authenticate, login


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
            
        

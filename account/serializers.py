from rest_framework import serializers
from .models import CustomUser
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    password2 = serializers.CharField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'message': 'Passwords do not match'})
        
        return super().validate(data)
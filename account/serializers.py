from rest_framework import serializers
from .models import CustomUser
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password2 = serializers.CharField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
        'password': {'write_only': True},
        'password2': {'write_only': True}
    }
        
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'message': 'Passwords do not match'})
        
        return super().validate(data)
    
    def create(self, validated_data):
        validated_data.pop('password2')
        return super().create(validated_data)

class EditUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'password']
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'username': {'required': False},
            'password': {'write_only': True, 'required': False}
            
        }

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'username': {'required': True}
        }
    
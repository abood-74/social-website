from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Contact
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    

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
        validated_data['password'] = make_password(validated_data['password'])
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
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'username': {'required': True}
        }
    
    def create(self, validated_data):
        
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class AuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)

class UserFollowSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    
    def validate(self, data):
        if data['action'] not in ['follow', 'unfollow']:
            raise serializers.ValidationError({'message': 'Invalid action'})
        
        return super().validate(data)
    

class UserDashboardSerializer(serializers.ModelSerializer):
    following = UserSerializer(many=True)
    followers = UserSerializer(many=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'following', 'followers']
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'username': {'required': False}
        }
    
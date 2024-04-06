from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Image
        fields = ['slug', 'url', 'image', 'title', 'description', 'created', 'users_like', 'user']
        extra_kwargs = {
            'image': {'required': False},
            'users_like': {'required': False},
            'created': {'required': False},
            'description': {'required': False},
            'title': {'required': False},
            'user': {'required': False},
        }
        
    
    def validate(self, data):
        url = data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()[:3]
        print(extension)
        
        if extension not in valid_extensions:
            raise serializers.ValidationError("The given URL does not match valid image extensions.")
        if Image.objects.filter(url=url).exists():
                raise serializers.ValidationError("This image has already been uploaded.")
        
        return super().validate(data)
    
    

class ImageDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = ['slug', 'url', 'image', 'title', 'description', 'created', 'users_like', 'user']
        extra_kwargs = {
            'slug': {'required': False},
            'image': {'required': False},
            'users_like': {'required': False},
            'created': {'required': False},
            'description': {'required': False},
            'title': {'required': False},
            'user': {'required': False},
            'url': {'required': False},
            
        }
        
    def validate(self, data):
        if 'url' in data:
            url = data['url']
            valid_extensions = ['jpg', 'jpeg', 'png']
            extension = url.rsplit('.', 1)[1].lower()[:3]
            
            if extension not in valid_extensions:
                raise serializers.ValidationError("The given URL does not match valid image extensions.")
            if Image.objects.filter(url=url).exists():
                    raise serializers.ValidationError("This image has already been uploaded.")
            
            return super().validate(data)
        else:
            return super().validate(data)
        

class ImageLikeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    
    def validate(self, data):
        if data['action'] not in ['like', 'unlike']:
            raise serializers.ValidationError("Invalid action")
        return super().validate(data)
        
        
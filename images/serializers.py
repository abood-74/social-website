from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Image
        fields = ['slug', 'url', 'image']
        extra_kwargs = {
            'image': {'required': False},
        }
        
    
    def validate(self, data):
        url = data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        
        if extension not in valid_extensions:
            raise serializers.ValidationError("The given URL does not match valid image extensions.")
        if Image.objects.filter(url=url).exists():
                raise serializers.ValidationError("This image has already been uploaded.")
        
        return super().validate(data)
    
    
        
        
        
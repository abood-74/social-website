from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
import requests
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
#local imports
from .serializers import ImageSerializer, ImageDetailSerializer, ImageLikeSerializer
from .models import Image


class ImageCreateAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            response = requests.get(url).content
            image = ContentFile(response, name=url.split('/')[-1])
            serializer.validated_data['image'] = image
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ImageDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            image = Image.objects.get(id=id)
            return Response(ImageDetailSerializer(image).data, status=status.HTTP_200_OK)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    
    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            image = Image.objects.get(id=id)
            serializer = ImageDetailSerializer(image, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    
    def patch(self, request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            image = Image.objects.get(id=id)
            serializer = ImageDetailSerializer(image, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            image = Image.objects.get(id=id)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ImageLikeAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def post(self, request, *args, **kwargs):
        serializer = ImageLikeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                
                id = serializer.validated_data['id']
                image = Image.objects.get(id=id)
                if serializer.validated_data['action']  == 'like':
                    image.users_like.add(request.user)
                else:
                    image.users_like.remove(request.user)
                return Response(status=status.HTTP_200_OK)
            except Image.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    pagination_class = LimitOffsetPagination
    def get(self, request, *args, **kwargs):
        images = Image.objects.all()
        paginator = self.pagination_class()
        paginated_images = paginator.paginate_queryset(images, request)
        serializer = ImageDetailSerializer(paginated_images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
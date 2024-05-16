import redis

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
import requests
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from drf_yasg.utils import swagger_auto_schema
#local imports
from .serializers import ImageSerializer, ImageDetailSerializer, ImageLikeSerializer, ImageDetailWithTotalViewsSerializer
from .models import Image
from actions.utils import create_action
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST,
port=settings.REDIS_PORT,
db=settings.REDIS_DB)

class ImageCreateAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    
    @swagger_auto_schema(request_body=ImageSerializer, responses={201: ImageSerializer})
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            response = requests.get(url).content
            image = ContentFile(response, name=url.split('/')[-1])
            serializer.validated_data['image'] = image
            serializer.validated_data['user'] = request.user
            serializer.save()
            create_action(request.user, 'bookmarked image', serializer.instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ImageDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    
    @swagger_auto_schema(responses={200: ImageDetailWithTotalViewsSerializer})
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            image = Image.objects.get(id=id)
            image.total_views = r.incr(f'image:{image.id}:views')
            r.zincrby('image_ranking', 1, image.id)
            return Response(ImageDetailWithTotalViewsSerializer(image).data, status=status.HTTP_200_OK)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    
    @swagger_auto_schema(request_body=ImageDetailSerializer, responses={200: ImageDetailSerializer})
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

    @swagger_auto_schema(request_body=ImageDetailSerializer, responses={200: ImageDetailSerializer})
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
    
    @swagger_auto_schema(responses={204: 'No Content'})
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
    
    @swagger_auto_schema(request_body=ImageLikeSerializer, responses={200: 'OK'})
    def post(self, request, *args, **kwargs):
        serializer = ImageLikeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                
                id = serializer.validated_data['id']
                image = Image.objects.get(id=id)
                if serializer.validated_data['action']  == 'like':
                    image.users_like.add(request.user)
                    create_action(request.user, 'liked image', image)
                else:
                    image.users_like.remove(request.user)
                return Response(status=status.HTTP_200_OK)
            except Image.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    pagination_class = LimitOffsetPagination
    
    @swagger_auto_schema(responses={200: ImageDetailSerializer})
    def get(self, request, *args, **kwargs):
        images = Image.objects.all()
        paginator = self.pagination_class()
        paginated_images = paginator.paginate_queryset(images, request)
        serializer = ImageDetailSerializer(paginated_images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ImageRankingAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    
    @swagger_auto_schema(responses={200: ImageDetailSerializer})
    def get(self, request, *args, **kwargs):
        image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
        image_ranking_ids = [int(id) for id in image_ranking]
        most_viewed_images = list(Image.objects.filter(id__in=image_ranking_ids))
        most_viewed_images.sort(key=lambda x: image_ranking_ids.index(x.id))
        serializer = ImageDetailSerializer(most_viewed_images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
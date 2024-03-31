from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
import requests
#local imports
from .serializers import ImageSerializer


class ImageCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            response = requests.get(url).content
            image = ContentFile(response, name=url.split('/')[-1])
            serializer.validated_data['image'] = image
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


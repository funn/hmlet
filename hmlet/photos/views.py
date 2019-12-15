from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Photo
from .serializers import PhotoSerializer


class PhotoView(ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


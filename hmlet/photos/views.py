from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Photo
from .serializers import PhotoSerializer


class PhotoView(ModelViewSet):
    lookup_field = 'uuid'
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def filter_queryset(self, queryset):
        if self.request.method == 'DELETE':
            queryset = queryset.filter(uploaded_by=self.request.user)  # Only allow to delete own photos

        return super().filter_queryset(queryset)


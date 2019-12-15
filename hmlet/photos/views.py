from django_filters import rest_framework as filters

from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Photo
from .serializers import PhotoSerializer


class PhotoFilter(filters.FilterSet):
    status = filters.CharFilter(method='status_filter')

    def status_filter(self, queryset, name, value):
        return queryset.filter(status=value).filter(uploaded_by=self.request.user)


class PhotoView(ModelViewSet):
    lookup_field = 'uuid'
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filterset_class = PhotoFilter
    filter_backends = [OrderingFilter, filters.DjangoFilterBackend]
    ordering_fields = ['status_changed']

    def filter_queryset(self, queryset):
        if self.request.method in ['DELETE', 'PUT']:
            queryset = queryset.filter(uploaded_by=self.request.user)  # Only allow to modify own photos

        return super().filter_queryset(queryset)


from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.SlugRelatedField(slug_field='uuid', required=False, queryset=get_user_model().objects.all(), help_text='UUID of the user who uploaded the photo.')

    class Meta:
        model = Photo
        fields = ['uploaded_by', 'image', 'captions']
        read_only_fields = ['uploaded_by']

    def validate_image(self, value):
        if self.instance: raise ValidationError('Can\'t change already uploaded image file')
        return value

    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


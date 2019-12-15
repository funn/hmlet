from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.SlugRelatedField(slug_field='uuid', required=False, queryset=get_user_model().objects.all(), help_text='UUID of the user who uploaded the photo.')
    image = serializers.ImageField(required=False, help_text='Photo image file.')

    class Meta:
        model = Photo
        fields = ['uuid', 'uploaded_by', 'status', 'image', 'captions', 'status_changed']
        read_only_fields = ['uuid', 'uploaded_by']

    def validate_image(self, value):
        if self.instance:
            raise ValidationError('Can\'t change already uploaded image file.')
        return value

    def validate_status(self, value):
        if self.instance and value == 'draft':
            raise ValidationError('Can\'t make already published photo a draft.')
        return value

    def validate(self, attrs):
        if not self.instance and not attrs.get('image'):
            raise ValidationError('No image was submitted.')
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


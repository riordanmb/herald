"""
Serializers for Markup app.
"""

from rest_framework import serializers
from .models import Annotation


class AnnotationSerializer(serializers.ModelSerializer):
    """Serializer for Annotation model."""
    
    surrogate_display_name = serializers.CharField(
        source='surrogate.get_display_name',
        read_only=True
    )
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True
    )

    class Meta:
        model = Annotation
        fields = [
            'id',
            'surrogate',
            'surrogate_display_name',
            'annotation_type',
            'coordinates',
            'label',
            'category',
            'description',
            'related_arms_id',
            'related_transcription_id',
            'tags',
            'color',
            'stroke_width',
            'created_at',
            'updated_at',
            'created_by_username',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_username', 'surrogate_display_name']


class AnnotationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating annotations."""
    
    class Meta:
        model = Annotation
        fields = [
            'surrogate',
            'annotation_type',
            'coordinates',
            'label',
            'category',
            'description',
            'related_arms_id',
            'related_transcription_id',
            'tags',
            'color',
            'stroke_width',
        ]

    def validate_coordinates(self, value):
        """Validate coordinates based on annotation type."""
        if not isinstance(value, (dict, list)):
            raise serializers.ValidationError("Coordinates must be a dict or list")
        return value

    def create(self, validated_data):
        """Create annotation with current user as creator."""
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


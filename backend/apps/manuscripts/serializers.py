"""
Serializers for Manuscripts app.
"""

from rest_framework import serializers
from .models import Manuscript, Surrogate


class SurrogateSerializer(serializers.ModelSerializer):
    """Serializer for Surrogate model."""

    display_name = serializers.CharField(source='get_display_name', read_only=True)

    class Meta:
        model = Surrogate
        fields = [
            'id',
            'manuscript',
            'surrogate_type',
            'folio_number',
            'sequence_number',
            'image_url',
            'thumbnail_url',
            'iiif_manifest',
            'width',
            'height',
            'dpi',
            'file_format',
            'file_size',
            'capture_date',
            'photographer',
            'copyright_holder',
            'license',
            'notes',
            'created_at',
            'display_name',
        ]
        read_only_fields = ['id', 'created_at', 'display_name']


class SurrogateCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating surrogates with file upload."""
    
    image = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = Surrogate
        fields = [
            'manuscript',
            'surrogate_type',
            'folio_number',
            'sequence_number',
            'image',
            'dpi',
            'capture_date',
            'photographer',
            'copyright_holder',
            'license',
            'notes',
        ]
    
    def validate_image(self, value):
        """Validate uploaded image."""
        # Check file size (max 50MB)
        if value.size > 50 * 1024 * 1024:
            raise serializers.ValidationError("Image file too large. Maximum size is 50MB.")
        
        # Check file type
        if not value.content_type.startswith('image/'):
            raise serializers.ValidationError("File must be an image.")
        
        return value


class ManuscriptListSerializer(serializers.ModelSerializer):
    """Simplified serializer for manuscript lists."""

    surrogate_count = serializers.IntegerField(
        source='surrogates.count',
        read_only=True
    )
    date_range = serializers.CharField(
        source='get_date_range',
        read_only=True
    )

    class Meta:
        model = Manuscript
        fields = [
            'id',
            'shelfmark',
            'repository',
            'collection',
            'date_range',
            'date_display',
            'material',
            'folios',
            'language',
            'script',
            'surrogate_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'date_range']


class ManuscriptDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for manuscript with all fields and related surrogates."""

    surrogates = SurrogateSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True
    )
    date_range = serializers.CharField(
        source='get_date_range',
        read_only=True
    )

    class Meta:
        model = Manuscript
        fields = [
            'id',
            'shelfmark',
            'repository',
            'collection',
            'alternative_names',
            'material',
            'dimensions',
            'folios',
            'date_earliest',
            'date_latest',
            'date_display',
            'date_range',
            'origin_location',
            'provenance',
            'language',
            'script',
            'content_summary',
            'bibliography',
            'created_at',
            'updated_at',
            'created_by_username',
            'surrogates',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_username', 'date_range']


class ManuscriptCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating manuscripts."""

    class Meta:
        model = Manuscript
        fields = [
            'shelfmark',
            'repository',
            'collection',
            'alternative_names',
            'material',
            'dimensions',
            'folios',
            'date_earliest',
            'date_latest',
            'date_display',
            'origin_location',
            'provenance',
            'language',
            'script',
            'content_summary',
            'bibliography',
        ]

    def create(self, validated_data):
        """Create manuscript with current user as creator."""
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class ManuscriptUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating manuscripts."""

    class Meta:
        model = Manuscript
        fields = [
            'shelfmark',
            'repository',
            'collection',
            'alternative_names',
            'material',
            'dimensions',
            'folios',
            'date_earliest',
            'date_latest',
            'date_display',
            'origin_location',
            'provenance',
            'language',
            'script',
            'content_summary',
            'bibliography',
        ]

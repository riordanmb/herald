"""
Views for Manuscripts app.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Manuscript, Surrogate
from .serializers import (
    ManuscriptListSerializer,
    ManuscriptDetailSerializer,
    ManuscriptCreateSerializer,
    ManuscriptUpdateSerializer,
    SurrogateSerializer,
    SurrogateCreateSerializer,
)
from .storage import get_storage


class ManuscriptViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Manuscript model.

    Provides CRUD operations for manuscripts.
    """
    queryset = Manuscript.objects.prefetch_related('surrogates').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering
    filterset_fields = {
        'repository': ['exact', 'icontains'],
        'material': ['exact'],
        'language': ['exact'],
        'script': ['exact'],
        'date_earliest': ['gte', 'lte'],
        'date_latest': ['gte', 'lte'],
    }

    # Search
    search_fields = [
        'shelfmark',
        'repository',
        'collection',
        'content_summary',
        'origin_location',
    ]

    # Ordering
    ordering_fields = [
        'shelfmark',
        'repository',
        'date_earliest',
        'created_at',
        'updated_at',
    ]
    ordering = ['repository', 'shelfmark']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return ManuscriptListSerializer
        elif self.action == 'create':
            return ManuscriptCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ManuscriptUpdateSerializer
        return ManuscriptDetailSerializer

    def get_queryset(self):
        """
        Optionally filter queryset by query parameters.
        """
        queryset = super().get_queryset()

        # Filter by date range
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if date_from:
            queryset = queryset.filter(
                Q(date_latest__gte=date_from) | Q(date_earliest__gte=date_from)
            )
        if date_to:
            queryset = queryset.filter(
                Q(date_earliest__lte=date_to) | Q(date_latest__lte=date_to)
            )

        return queryset

    @action(detail=True, methods=['get'])
    def surrogates(self, request, pk=None):
        """
        Get all surrogates for a manuscript.
        """
        manuscript = self.get_object()
        surrogates = manuscript.surrogates.all()
        serializer = SurrogateSerializer(surrogates, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def relationships(self, request, pk=None):
        """
        Get manuscript relationships (for future recession tracking).
        Placeholder for Phase 5.
        """
        return Response({
            'source_relationships': [],
            'target_relationships': [],
        })


class SurrogateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Surrogate model.

    Provides CRUD operations for manuscript surrogates.
    """
    queryset = Surrogate.objects.select_related('manuscript').all()
    serializer_class = SurrogateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering
    filterset_fields = {
        'manuscript': ['exact'],
        'surrogate_type': ['exact'],
        'folio_number': ['exact', 'icontains'],
        'file_format': ['exact'],
    }

    # Search
    search_fields = [
        'manuscript__shelfmark',
        'folio_number',
        'photographer',
    ]

    # Ordering
    ordering_fields = [
        'folio_number',
        'sequence_number',
        'created_at',
    ]
    ordering = ['folio_number', 'sequence_number']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return SurrogateCreateSerializer
        return SurrogateSerializer

    def get_queryset(self):
        """
        Optionally filter queryset by manuscript.
        """
        queryset = super().get_queryset()

        # Filter by manuscript (from URL param)
        manuscript_id = self.request.query_params.get('manuscript_id')
        if manuscript_id:
            queryset = queryset.filter(manuscript_id=manuscript_id)

        return queryset
    
    def create(self, request, *args, **kwargs):
        """Create surrogate with image upload."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get image file
        image_file = serializer.validated_data.pop('image')
        manuscript = serializer.validated_data['manuscript']
        folio_number = serializer.validated_data['folio_number']
        sequence_number = serializer.validated_data.get('sequence_number', 1)
        
        # Upload to MinIO
        storage = get_storage()
        upload_result = storage.upload_image(
            image_file,
            str(manuscript.id),
            folio_number,
            sequence_number
        )
        
        # Create surrogate with uploaded URLs
        surrogate = Surrogate.objects.create(
            **serializer.validated_data,
            image_url=upload_result['image_url'],
            thumbnail_url=upload_result['thumbnail_url'],
            width=upload_result['width'],
            height=upload_result['height'],
            file_size=upload_result['file_size'],
            file_format='JPEG',
        )
        
        response_serializer = SurrogateSerializer(surrogate)
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def destroy(self, request, *args, **kwargs):
        """Delete surrogate and associated images."""
        surrogate = self.get_object()
        manuscript_id = str(surrogate.manuscript.id)
        folio_number = surrogate.folio_number
        sequence_number = surrogate.sequence_number
        
        # Delete from storage
        storage = get_storage()
        storage.delete_image(manuscript_id, folio_number, sequence_number)
        
        # Delete surrogate
        return super().destroy(request, *args, **kwargs)

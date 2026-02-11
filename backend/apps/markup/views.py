"""
Views for Markup app.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .models import Annotation
from .serializers import (
    AnnotationSerializer,
    AnnotationCreateSerializer,
)


class AnnotationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Annotation model.
    
    Provides CRUD operations for annotations on manuscript images.
    """
    queryset = Annotation.objects.select_related(
        'surrogate',
        'surrogate__manuscript',
        'created_by'
    ).all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering
    filterset_fields = {
        'surrogate': ['exact'],
        'annotation_type': ['exact'],
        'category': ['exact', 'icontains'],
        'created_by': ['exact'],
    }

    # Search
    search_fields = [
        'label',
        'description',
        'category',
    ]

    # Ordering
    ordering_fields = [
        'created_at',
        'updated_at',
        'label',
    ]
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return AnnotationCreateSerializer
        return AnnotationSerializer

    def get_queryset(self):
        """Optionally filter queryset by surrogate."""
        queryset = super().get_queryset()
        
        # Filter by surrogate (from URL param)
        surrogate_id = self.request.query_params.get('surrogate_id')
        if surrogate_id:
            queryset = queryset.filter(surrogate_id=surrogate_id)
        
        return queryset

    @action(detail=False, methods=['get'])
    def by_surrogate(self, request):
        """
        Get all annotations for a specific surrogate.
        
        GET /api/v1/markup/annotations/by_surrogate/?surrogate_id=<uuid>
        """
        surrogate_id = request.query_params.get('surrogate_id')
        if not surrogate_id:
            return Response(
                {'error': 'surrogate_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        annotations = self.get_queryset().filter(surrogate_id=surrogate_id)
        serializer = self.get_serializer(annotations, many=True)
        return Response(serializer.data)

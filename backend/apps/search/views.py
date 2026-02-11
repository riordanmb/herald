"""
Views for Search app.
"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema

@extend_schema(exclude=True)
@api_view(['GET'])
def placeholder_view(request):
    """
    Placeholder view for Search app.
    Will be implemented in future phases.
    """
    return Response({
        'message': 'Search API coming soon',
        'status': 'planned'
    })

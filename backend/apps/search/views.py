"""
Views for Search app.
"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

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

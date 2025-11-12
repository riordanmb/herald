"""
Views for Recession app.
"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def placeholder_view(request):
    """
    Placeholder view for Recession app.
    Will be implemented in future phases.
    """
    return Response({
        'message': 'Recession API coming soon',
        'status': 'planned'
    })

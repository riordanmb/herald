"""
URL routing for Markup app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnotationViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'annotations', AnnotationViewSet, basename='annotation')

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]

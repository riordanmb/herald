"""
URL routing for Manuscripts app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManuscriptViewSet, SurrogateViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'manuscripts', ManuscriptViewSet, basename='manuscript')
router.register(r'surrogates', SurrogateViewSet, basename='surrogate')

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]

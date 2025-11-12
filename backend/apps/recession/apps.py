"""
Recession app configuration.
"""

from django.apps import AppConfig


class RecessionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.recession'
    verbose_name = 'Recession'

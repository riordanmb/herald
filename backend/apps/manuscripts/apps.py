"""
Manuscripts app configuration.
"""

from django.apps import AppConfig


class ManuscriptsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.manuscripts'
    verbose_name = 'Manuscripts'

    def ready(self):
        """Import signal handlers when app is ready."""
        try:
            import apps.manuscripts.signals  # noqa
        except ImportError:
            pass

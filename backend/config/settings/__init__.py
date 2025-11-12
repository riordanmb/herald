"""
Django settings module selector.
Automatically loads the appropriate settings based on DJANGO_SETTINGS_MODULE.
"""

import os

# Determine which settings to use
ENVIRONMENT = os.getenv('DJANGO_ENV', 'development')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'development':
    from .development import *
else:
    from .base import *

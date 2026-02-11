"""
Admin configuration for authentication app.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

# Unregister the default User admin if it's already registered
if admin.site.is_registered(User):
    admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin with additional fields."""
    
    list_display = BaseUserAdmin.list_display
    list_filter = BaseUserAdmin.list_filter
    
    # date_joined is already included in BaseUserAdmin fieldsets
    # No need to add it again


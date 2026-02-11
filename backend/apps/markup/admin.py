"""
Admin configuration for Markup app.
"""

from django.contrib import admin
from .models import Annotation


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    """Admin interface for Annotation model."""

    list_display = [
        'label',
        'surrogate',
        'annotation_type',
        'category',
        'created_by',
        'created_at',
    ]

    list_filter = [
        'annotation_type',
        'category',
        'created_at',
    ]

    search_fields = [
        'label',
        'description',
        'surrogate__manuscript__shelfmark',
        'surrogate__folio_number',
    ]

    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'created_by',
    ]

    fieldsets = [
        ('Target', {
            'fields': ['surrogate']
        }),
        ('Geometry', {
            'fields': [
                'annotation_type',
                'coordinates',
            ]
        }),
        ('Content', {
            'fields': [
                'label',
                'category',
                'description',
                'tags',
            ]
        }),
        ('Styling', {
            'fields': [
                'color',
                'stroke_width',
            ],
            'classes': ['collapse'],
        }),
        ('Relations', {
            'fields': [
                'related_arms_id',
                'related_transcription_id',
            ],
            'classes': ['collapse'],
        }),
        ('Metadata', {
            'fields': [
                'id',
                'created_at',
                'updated_at',
                'created_by',
            ],
            'classes': ['collapse'],
        }),
    ]

    def save_model(self, request, obj, form, change):
        """Set created_by on new objects."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

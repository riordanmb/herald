"""
Admin configuration for Manuscripts app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Manuscript, Surrogate


class SurrogateInline(admin.TabularInline):
    """Inline admin for surrogates."""
    model = Surrogate
    extra = 0
    fields = ['folio_number', 'surrogate_type', 'width', 'height', 'created_at']
    readonly_fields = ['created_at']
    can_delete = True


@admin.register(Manuscript)
class ManuscriptAdmin(admin.ModelAdmin):
    """Admin interface for Manuscript model."""

    list_display = [
        'shelfmark',
        'repository',
        'date_display',
        'folios',
        'material',
        'surrogate_count',
        'created_at',
    ]

    list_filter = [
        'repository',
        'material',
        'language',
        'script',
        'created_at',
    ]

    search_fields = [
        'shelfmark',
        'repository',
        'collection',
        'content_summary',
        'origin_location',
    ]

    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'created_by',
    ]

    fieldsets = [
        ('Identification', {
            'fields': [
                'id',
                'shelfmark',
                'repository',
                'collection',
                'alternative_names',
            ]
        }),
        ('Physical Description', {
            'fields': [
                'material',
                'dimensions',
                'folios',
            ]
        }),
        ('Dating & Provenance', {
            'fields': [
                'date_earliest',
                'date_latest',
                'date_display',
                'origin_location',
                'provenance',
            ]
        }),
        ('Content', {
            'fields': [
                'language',
                'script',
                'content_summary',
            ]
        }),
        ('Bibliography', {
            'fields': ['bibliography'],
            'classes': ['collapse'],
        }),
        ('Metadata', {
            'fields': [
                'created_at',
                'updated_at',
                'created_by',
            ],
            'classes': ['collapse'],
        }),
    ]

    inlines = [SurrogateInline]

    def surrogate_count(self, obj):
        """Display number of surrogates."""
        count = obj.surrogates.count()
        return format_html(
            '<span style="color: {};">{} surrogates</span>',
            'green' if count > 0 else 'gray',
            count
        )
    surrogate_count.short_description = 'Surrogates'

    def save_model(self, request, obj, form, change):
        """Set created_by on new objects."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Surrogate)
class SurrogateAdmin(admin.ModelAdmin):
    """Admin interface for Surrogate model."""

    list_display = [
        'get_display_name',
        'surrogate_type',
        'folio_number',
        'width',
        'height',
        'file_format',
        'created_at',
    ]

    list_filter = [
        'surrogate_type',
        'file_format',
        'created_at',
    ]

    search_fields = [
        'manuscript__shelfmark',
        'manuscript__repository',
        'folio_number',
        'photographer',
    ]

    readonly_fields = [
        'id',
        'created_at',
        'image_preview',
    ]

    fieldsets = [
        ('Manuscript', {
            'fields': ['manuscript']
        }),
        ('Type & Identification', {
            'fields': [
                'surrogate_type',
                'folio_number',
                'sequence_number',
            ]
        }),
        ('Image', {
            'fields': [
                'image_url',
                'thumbnail_url',
                'iiif_manifest',
                'image_preview',
            ]
        }),
        ('Technical Metadata', {
            'fields': [
                'width',
                'height',
                'dpi',
                'file_format',
                'file_size',
            ]
        }),
        ('Capture Information', {
            'fields': [
                'capture_date',
                'photographer',
                'copyright_holder',
                'license',
            ],
            'classes': ['collapse'],
        }),
        ('Notes', {
            'fields': ['notes'],
            'classes': ['collapse'],
        }),
        ('Metadata', {
            'fields': ['id', 'created_at'],
            'classes': ['collapse'],
        }),
    ]

    def image_preview(self, obj):
        """Display image preview."""
        if obj.thumbnail_url:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px;" />',
                obj.thumbnail_url
            )
        elif obj.image_url:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px;" />',
                obj.image_url
            )
        return "No image available"
    image_preview.short_description = 'Preview'

    def get_display_name(self, obj):
        """Get surrogate display name."""
        return obj.get_display_name()
    get_display_name.short_description = 'Surrogate'

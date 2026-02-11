"""
Models for Markup app - Annotations on manuscript images.
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Annotation(models.Model):
    """
    General-purpose annotation on a manuscript surrogate image.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Target surrogate
    surrogate = models.ForeignKey(
        'manuscripts.Surrogate',
        on_delete=models.CASCADE,
        related_name='annotations'
    )

    # Geometry
    ANNOTATION_TYPES = [
        ('point', 'Point'),
        ('rect', 'Rectangle'),
        ('polygon', 'Polygon'),
        ('circle', 'Circle'),
    ]
    annotation_type = models.CharField(
        max_length=20,
        choices=ANNOTATION_TYPES,
        help_text="Type of annotation shape"
    )
    coordinates = models.JSONField(
        help_text="Coordinates in format specific to annotation type"
    )

    # Content
    label = models.CharField(
        max_length=255,
        help_text="Short label for the annotation"
    )
    category = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Category of annotation (e.g., 'heraldry', 'text', 'decoration')"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the annotation"
    )

    # Optional links to other entities (will be enabled when those models exist)
    # related_arms = models.ForeignKey(
    #     'heraldry.Arms',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='annotations'
    # )
    # related_transcription = models.ForeignKey(
    #     'transcription.Transcription',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='annotations'
    # )
    # Store as UUID strings for now, will convert to ForeignKeys later
    related_arms_id = models.UUIDField(null=True, blank=True)
    related_transcription_id = models.UUIDField(null=True, blank=True)

    # Tags for organization
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text="List of tags for categorization"
    )

    # Visual styling (optional)
    color = models.CharField(
        max_length=7,
        default='#FF0000',
        help_text="Hex color code for annotation display"
    )
    stroke_width = models.IntegerField(
        default=2,
        help_text="Stroke width in pixels"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='annotations_created'
    )

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['surrogate', 'category']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Annotation'
        verbose_name_plural = 'Annotations'

    def __str__(self):
        return f"{self.label} on {self.surrogate.get_display_name()}"

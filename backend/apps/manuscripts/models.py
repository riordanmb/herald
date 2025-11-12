"""
Manuscript and Surrogate models.
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

User = get_user_model()


class Manuscript(models.Model):
    """
    Core manuscript entity representing a physical manuscript.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Identification
    shelfmark = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Manuscript shelfmark or catalog number"
    )
    repository = models.CharField(
        max_length=255,
        help_text="Institution or library holding the manuscript"
    )
    collection = models.CharField(
        max_length=255,
        blank=True,
        help_text="Collection within the repository"
    )
    alternative_names = models.JSONField(
        default=list,
        blank=True,
        help_text="Alternative names or identifiers"
    )

    # Physical description
    MATERIAL_CHOICES = [
        ('parchment', 'Parchment'),
        ('paper', 'Paper'),
        ('mixed', 'Mixed'),
        ('vellum', 'Vellum'),
        ('other', 'Other'),
    ]
    material = models.CharField(
        max_length=50,
        choices=MATERIAL_CHOICES,
        default='parchment'
    )
    dimensions = models.JSONField(
        default=dict,
        blank=True,
        help_text="Dimensions in format: {height: X, width: Y, unit: 'mm'}"
    )
    folios = models.IntegerField(
        help_text="Number of folios"
    )

    # Dating & provenance
    date_earliest = models.IntegerField(
        null=True,
        blank=True,
        help_text="Earliest possible date"
    )
    date_latest = models.IntegerField(
        null=True,
        blank=True,
        help_text="Latest possible date"
    )
    date_display = models.CharField(
        max_length=100,
        help_text="Human-readable date (e.g., 'late 14th century')"
    )
    origin_location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Place of origin"
    )
    provenance = models.TextField(
        blank=True,
        help_text="Ownership history"
    )

    # Content
    language = models.CharField(
        max_length=50,
        default='Latin',
        help_text="Primary language"
    )
    script = models.CharField(
        max_length=50,
        default='Gothic',
        help_text="Script type"
    )
    content_summary = models.TextField(
        help_text="Brief summary of contents"
    )

    # Bibliography
    bibliography = models.JSONField(
        default=list,
        blank=True,
        help_text="List of bibliographic references"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='manuscripts_created'
    )

    # Full-text search
    search_vector = SearchVectorField(null=True, editable=False)

    class Meta:
        ordering = ['repository', 'shelfmark']
        indexes = [
            models.Index(fields=['repository', 'shelfmark']),
            models.Index(fields=['date_earliest', 'date_latest']),
            models.Index(fields=['created_at']),
            GinIndex(fields=['search_vector']),
        ]
        verbose_name = 'Manuscript'
        verbose_name_plural = 'Manuscripts'

    def __str__(self):
        return f"{self.repository}, {self.shelfmark}"

    def get_date_range(self):
        """Return formatted date range."""
        if self.date_earliest and self.date_latest:
            if self.date_earliest == self.date_latest:
                return str(self.date_earliest)
            return f"{self.date_earliest}-{self.date_latest}"
        return self.date_display


class Surrogate(models.Model):
    """
    Photos, prints, and other representations of manuscripts.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    manuscript = models.ForeignKey(
        Manuscript,
        on_delete=models.CASCADE,
        related_name='surrogates'
    )

    # Type
    SURROGATE_TYPES = [
        ('photo', 'Photograph'),
        ('scan', 'Digital Scan'),
        ('print', 'Printed Edition'),
        ('facsimile', 'Facsimile'),
        ('derivative', 'Derivative Work'),
    ]
    surrogate_type = models.CharField(
        max_length=20,
        choices=SURROGATE_TYPES,
        default='photo'
    )

    # Identification
    folio_number = models.CharField(
        max_length=20,
        help_text="Folio reference (e.g., '12r', '45v')"
    )
    sequence_number = models.IntegerField(
        default=1,
        help_text="Sequence number for multiple surrogates of same folio"
    )

    # Image storage
    image_url = models.URLField(
        max_length=500,
        help_text="URL to image file in object storage"
    )
    thumbnail_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="URL to thumbnail image"
    )
    iiif_manifest = models.URLField(
        max_length=500,
        blank=True,
        help_text="IIIF manifest URL"
    )

    # Technical metadata
    width = models.IntegerField(help_text="Image width in pixels")
    height = models.IntegerField(help_text="Image height in pixels")
    dpi = models.IntegerField(
        null=True,
        blank=True,
        help_text="Dots per inch"
    )
    file_format = models.CharField(
        max_length=10,
        default='JPEG',
        help_text="Image file format"
    )
    file_size = models.BigIntegerField(
        help_text="File size in bytes"
    )

    # Capture information
    capture_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date image was captured"
    )
    photographer = models.CharField(
        max_length=255,
        blank=True,
        help_text="Name of photographer"
    )
    copyright_holder = models.CharField(
        max_length=255,
        blank=True,
        help_text="Copyright holder"
    )
    license = models.CharField(
        max_length=100,
        blank=True,
        help_text="License terms (e.g., CC-BY-4.0)"
    )

    # Notes
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about this surrogate"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['folio_number', 'sequence_number']
        unique_together = [['manuscript', 'folio_number', 'sequence_number']]
        indexes = [
            models.Index(fields=['manuscript', 'folio_number']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Surrogate'
        verbose_name_plural = 'Surrogates'

    def __str__(self):
        return f"{self.manuscript.shelfmark}, folio {self.folio_number}"

    def get_display_name(self):
        """Return display name for this surrogate."""
        name = f"{self.manuscript.shelfmark}, {self.folio_number}"
        if self.sequence_number > 1:
            name += f" ({self.sequence_number})"
        return name

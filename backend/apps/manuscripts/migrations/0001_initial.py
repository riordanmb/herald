# Generated migration for Manuscript and Surrogate models

import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.contrib.postgres.indexes
import django.contrib.postgres.search


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Manuscript',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('shelfmark', models.CharField(db_index=True, help_text='Manuscript shelfmark or catalog number', max_length=255)),
                ('repository', models.CharField(help_text='Institution or library holding the manuscript', max_length=255)),
                ('collection', models.CharField(blank=True, help_text='Collection within the repository', max_length=255)),
                ('alternative_names', models.JSONField(blank=True, default=list, help_text='Alternative names or identifiers')),
                ('material', models.CharField(choices=[('parchment', 'Parchment'), ('paper', 'Paper'), ('mixed', 'Mixed'), ('vellum', 'Vellum'), ('other', 'Other')], default='parchment', max_length=50)),
                ('dimensions', models.JSONField(blank=True, default=dict, help_text="Dimensions in format: {height: X, width: Y, unit: 'mm'}")),
                ('folios', models.IntegerField(help_text='Number of folios')),
                ('date_earliest', models.IntegerField(blank=True, help_text='Earliest possible date', null=True)),
                ('date_latest', models.IntegerField(blank=True, help_text='Latest possible date', null=True)),
                ('date_display', models.CharField(help_text="Human-readable date (e.g., 'late 14th century')", max_length=100)),
                ('origin_location', models.CharField(blank=True, help_text='Place of origin', max_length=255)),
                ('provenance', models.TextField(blank=True, help_text='Ownership history')),
                ('language', models.CharField(default='Latin', help_text='Primary language', max_length=50)),
                ('script', models.CharField(default='Gothic', help_text='Script type', max_length=50)),
                ('content_summary', models.TextField(help_text='Brief summary of contents')),
                ('bibliography', models.JSONField(blank=True, default=list, help_text='List of bibliographic references')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(editable=False, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='manuscripts_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Manuscript',
                'verbose_name_plural': 'Manuscripts',
                'ordering': ['repository', 'shelfmark'],
            },
        ),
        migrations.CreateModel(
            name='Surrogate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('surrogate_type', models.CharField(choices=[('photo', 'Photograph'), ('scan', 'Digital Scan'), ('print', 'Printed Edition'), ('facsimile', 'Facsimile'), ('derivative', 'Derivative Work')], default='photo', max_length=20)),
                ('folio_number', models.CharField(help_text="Folio reference (e.g., '12r', '45v')", max_length=20)),
                ('sequence_number', models.IntegerField(default=1, help_text='Sequence number for multiple surrogates of same folio')),
                ('image_url', models.URLField(help_text='URL to image file in object storage', max_length=500)),
                ('thumbnail_url', models.URLField(blank=True, help_text='URL to thumbnail image', max_length=500)),
                ('iiif_manifest', models.URLField(blank=True, help_text='IIIF manifest URL', max_length=500)),
                ('width', models.IntegerField(help_text='Image width in pixels')),
                ('height', models.IntegerField(help_text='Image height in pixels')),
                ('dpi', models.IntegerField(blank=True, help_text='Dots per inch', null=True)),
                ('file_format', models.CharField(default='JPEG', help_text='Image file format', max_length=10)),
                ('file_size', models.BigIntegerField(help_text='File size in bytes')),
                ('capture_date', models.DateField(blank=True, help_text='Date image was captured', null=True)),
                ('photographer', models.CharField(blank=True, help_text='Name of photographer', max_length=255)),
                ('copyright_holder', models.CharField(blank=True, help_text='Copyright holder', max_length=255)),
                ('license', models.CharField(blank=True, help_text='License terms (e.g., CC-BY-4.0)', max_length=100)),
                ('notes', models.TextField(blank=True, help_text='Additional notes about this surrogate')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('manuscript', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surrogates', to='manuscripts.manuscript')),
            ],
            options={
                'verbose_name': 'Surrogate',
                'verbose_name_plural': 'Surrogates',
                'ordering': ['folio_number', 'sequence_number'],
                'unique_together': {('manuscript', 'folio_number', 'sequence_number')},
            },
        ),
        migrations.AddIndex(
            model_name='manuscript',
            index=models.Index(fields=['repository', 'shelfmark'], name='manuscripts_reposit_idx'),
        ),
        migrations.AddIndex(
            model_name='manuscript',
            index=models.Index(fields=['date_earliest', 'date_latest'], name='manuscripts_date_ea_idx'),
        ),
        migrations.AddIndex(
            model_name='manuscript',
            index=models.Index(fields=['created_at'], name='manuscripts_created_idx'),
        ),
        migrations.AddIndex(
            model_name='manuscript',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='manuscripts_search__gin_idx'),
        ),
        migrations.AddIndex(
            model_name='surrogate',
            index=models.Index(fields=['manuscript', 'folio_number'], name='manuscripts_manuscri_idx'),
        ),
        migrations.AddIndex(
            model_name='surrogate',
            index=models.Index(fields=['created_at'], name='manuscripts_surrogate_created_idx'),
        ),
    ]


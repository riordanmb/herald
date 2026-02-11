"""
Storage utilities for manuscript surrogates.
Handles MinIO/S3 uploads and thumbnail generation.
"""

import uuid
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from PIL import Image
import io
from urllib.parse import urljoin


class MinIOStorage:
    """MinIO storage handler for surrogate images."""
    
    def __init__(self):
        self.endpoint = settings.MINIO_ENDPOINT
        self.access_key = settings.MINIO_ACCESS_KEY
        self.secret_key = settings.MINIO_SECRET_KEY
        self.bucket = settings.MINIO_BUCKET
        self.use_ssl = settings.MINIO_USE_SSL
        
        # Initialize S3 client
        self.client = boto3.client(
            's3',
            endpoint_url=f"{'https' if self.use_ssl else 'http'}://{self.endpoint}",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name='us-east-1',  # MinIO doesn't care about region
        )
        
        # Ensure bucket exists
        self._ensure_bucket()
    
    def _ensure_bucket(self):
        """Ensure the bucket exists, create if it doesn't."""
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except ClientError:
            # Bucket doesn't exist, create it
            try:
                self.client.create_bucket(Bucket=self.bucket)
            except ClientError as e:
                # Bucket might have been created by another process
                if e.response['Error']['Code'] != 'BucketAlreadyOwnedByYou':
                    raise
    
    def _generate_key(self, manuscript_id, folio_number, sequence_number, suffix=''):
        """Generate S3 key for surrogate image."""
        filename = f"{manuscript_id}/{folio_number}_{sequence_number}{suffix}.jpg"
        return f"surrogates/{filename}"
    
    def upload_image(self, file: UploadedFile, manuscript_id, folio_number, sequence_number):
        """
        Upload image to MinIO and return URLs.
        
        Returns:
            dict with 'image_url' and 'thumbnail_url'
        """
        # Generate unique keys
        image_key = self._generate_key(manuscript_id, folio_number, sequence_number)
        thumbnail_key = self._generate_key(manuscript_id, folio_number, sequence_number, '_thumb')
        
        # Read image
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Get image dimensions
        width, height = image.size
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save full image
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='JPEG', quality=95)
        image_buffer.seek(0)
        
        # Upload full image
        self.client.upload_fileobj(
            image_buffer,
            self.bucket,
            image_key,
            ExtraArgs={'ContentType': 'image/jpeg'}
        )
        
        # Generate thumbnail (max 300px on longest side)
        thumbnail = image.copy()
        thumbnail.thumbnail((300, 300), Image.Resampling.LANCZOS)
        thumb_buffer = io.BytesIO()
        thumbnail.save(thumb_buffer, format='JPEG', quality=85)
        thumb_buffer.seek(0)
        
        # Upload thumbnail
        self.client.upload_fileobj(
            thumb_buffer,
            self.bucket,
            thumbnail_key,
            ExtraArgs={'ContentType': 'image/jpeg'}
        )
        
        # Generate URLs
        base_url = f"{'https' if self.use_ssl else 'http'}://{self.endpoint}/{self.bucket}/"
        image_url = urljoin(base_url, image_key)
        thumbnail_url = urljoin(base_url, thumbnail_key)
        
        return {
            'image_url': image_url,
            'thumbnail_url': thumbnail_url,
            'width': width,
            'height': height,
            'file_size': len(image_data),
        }
    
    def delete_image(self, manuscript_id, folio_number, sequence_number):
        """Delete image and thumbnail from MinIO."""
        image_key = self._generate_key(manuscript_id, folio_number, sequence_number)
        thumbnail_key = self._generate_key(manuscript_id, folio_number, sequence_number, '_thumb')
        
        try:
            self.client.delete_object(Bucket=self.bucket, Key=image_key)
            self.client.delete_object(Bucket=self.bucket, Key=thumbnail_key)
        except ClientError:
            # Ignore errors if files don't exist
            pass


# Global storage instance
_storage = None

def get_storage():
    """Get or create storage instance."""
    global _storage
    if _storage is None:
        _storage = MinIOStorage()
    return _storage


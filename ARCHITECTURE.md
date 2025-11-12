# Herald - Heraldic Manuscript Management System
## Architectural Plan

## Executive Summary

Herald is a comprehensive digital platform for heraldic scholarship that enables researchers to:
- Catalog and manage heraldic manuscripts with rich metadata
- Track manuscript recession (lineage and copying relationships)
- View and annotate manuscript surrogates (photos, prints, derivatives)
- Compare coats of arms across manuscripts
- Transcribe medieval texts
- Mark up heraldic imagery according to heraldic laws
- Search heraldic content with sophisticated queries
- Analyze paleography to identify scribes and scribal schools

## System Architecture

### High-Level Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                    Frontend Layer (Next.js)                        │
│  ┌─────────────┬──────────────┬─────────────┬──────────────────┐ │
│  │ Manuscript  │ Arms         │ Heraldic    │ Paleography      │ │
│  │ Viewer      │ Comparison   │ Search      │ Analysis         │ │
│  └─────────────┴──────────────┴─────────────┴──────────────────┘ │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                    ┌───────┴────────┐
                    │  API Gateway   │
                    │   (optional)   │
                    └───────┬────────┘
                            │
        ┌───────────────────┼────────────────────┐
        │                   │                    │
        ▼                   ▼                    ▼
┌──────────────────┐ ┌─────────────────┐ ┌────────────────────┐
│  Core API        │ │  Paleography    │ │  Static Assets     │
│  (Django)        │ │  Service        │ │  Service           │
│                  │ │  (FastAPI)      │ │  (MinIO/S3)        │
│ - Manuscripts    │ │                 │ │                    │
│ - Arms/Blazons   │ │ - Embeddings    │ │ - Images           │
│ - Transcriptions │ │ - Similarity    │ │ - Manuscripts      │
│ - Recession      │ │ - Clustering    │ │ - Surrogates       │
│ - Markup         │ │ - Scribe ID     │ │                    │
│ - Search         │ │                 │ │                    │
└────────┬─────────┘ └────────┬────────┘ └────────┬───────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
  ┌─────────────┐      ┌──────────┐        ┌──────────┐
  │ PostgreSQL  │      │  Redis   │        │  Search  │
  │  (Primary)  │      │  (Cache) │        │  Index   │
  └─────────────┘      └──────────┘        └──────────┘
```

### Technology Stack

#### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5.x
- **UI Library**: React 18+
- **Styling**: Tailwind CSS 3.x + shadcn/ui components
- **State Management**: React Query (TanStack Query) + Zustand
- **Image Viewer**: OpenSeadragon or IIIF viewer for manuscript viewing
- **Canvas Library**: Fabric.js or Konva.js for annotation/markup
- **Forms**: React Hook Form + Zod validation
- **Drag & Drop**: dnd-kit for comparison interfaces

#### Backend - Core API
- **Framework**: Django 5.x
- **API**: Django REST Framework 3.14+
- **Database ORM**: Django ORM with custom managers
- **Authentication**: Django JWT or OAuth2
- **Storage**: django-storages for S3/MinIO integration
- **Search**: PostgreSQL full-text search (+ Elasticsearch optional)
- **Task Queue**: Celery with Redis broker (for async tasks)

#### Backend - Paleography Service
- **Framework**: FastAPI 0.115+
- **ML Framework**: PyTorch 2.4+ with Transformers
- **Vision Model**: DINOv2 (facebook/dinov2-base)
- **Image Processing**: OpenCV, Pillow, scikit-image
- **Clustering**: scikit-learn (Agglomerative, DBSCAN)
- **Embeddings**: numpy, Redis for caching

#### Data Layer
- **Primary Database**: PostgreSQL 16+ with extensions:
  - pg_trgm (trigram matching for fuzzy search)
  - uuid-ossp (UUID generation)
  - PostGIS (optional, for geographic data)
- **Cache**: Redis 7.x
- **Object Storage**: MinIO (self-hosted) or AWS S3
- **Search**: PostgreSQL full-text + optional Elasticsearch 8.x

#### DevOps & Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes-ready (optional)
- **Reverse Proxy**: Nginx or Caddy
- **Monitoring**: Prometheus + Grafana (optional)
- **Logging**: Structured logging with JSON output

## Directory Structure

```
herald/
├── docs/                           # Documentation
│   ├── api/                        # API documentation
│   ├── user-guide/                 # User guides
│   └── development/                # Development guides
│
├── frontend/                       # Next.js application
│   ├── src/
│   │   ├── app/                    # App router pages
│   │   │   ├── manuscripts/        # Manuscript management
│   │   │   ├── arms/               # Arms comparison
│   │   │   ├── search/             # Heraldic search
│   │   │   └── paleography/        # Paleography analysis
│   │   ├── components/             # React components
│   │   │   ├── manuscript/         # Manuscript viewer components
│   │   │   ├── heraldry/           # Heraldic markup components
│   │   │   ├── comparison/         # Arms comparison UI
│   │   │   └── common/             # Shared components
│   │   ├── lib/                    # Utilities
│   │   ├── hooks/                  # Custom React hooks
│   │   ├── types/                  # TypeScript types
│   │   └── stores/                 # State management
│   ├── public/                     # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   └── next.config.js
│
├── backend/                        # Django application
│   ├── config/                     # Django settings
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/                       # Django apps
│   │   ├── manuscripts/            # Manuscript management
│   │   │   ├── models.py           # Manuscript, Surrogate models
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── tests/
│   │   ├── heraldry/               # Heraldic data
│   │   │   ├── models.py           # Arms, Blazon, Tincture models
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── tests/
│   │   ├── recession/              # Manuscript relationships
│   │   │   ├── models.py           # ManuscriptRelation model
│   │   │   ├── views.py
│   │   │   └── tests/
│   │   ├── transcription/          # Text transcription
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   └── tests/
│   │   ├── markup/                 # Heraldic markup
│   │   │   ├── models.py           # Annotation, Region models
│   │   │   ├── views.py
│   │   │   └── tests/
│   │   └── search/                 # Search functionality
│   │       ├── views.py
│   │       ├── indexes.py
│   │       └── tests/
│   ├── manage.py
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── development.txt
│   │   └── production.txt
│   └── pytest.ini
│
├── paleography/                    # FastAPI paleography service
│   ├── app/
│   │   ├── main.py                 # FastAPI app
│   │   ├── vision.py               # DINOv2 embeddings
│   │   ├── metrics.py              # Distance & clustering
│   │   ├── store.py                # Storage layer
│   │   ├── models.py               # Pydantic models
│   │   └── config.py               # Configuration
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── infrastructure/                 # Infrastructure as code
│   ├── docker/
│   │   ├── docker-compose.yml      # Development compose
│   │   ├── docker-compose.prod.yml # Production compose
│   │   ├── nginx/                  # Nginx config
│   │   └── postgres/               # Postgres init scripts
│   ├── kubernetes/                 # K8s manifests (optional)
│   └── terraform/                  # Cloud infrastructure (optional)
│
├── scripts/                        # Utility scripts
│   ├── setup-dev.sh
│   ├── backup-db.sh
│   └── seed-data.py
│
├── .github/                        # GitHub workflows
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── .gitignore
├── README.md
└── LICENSE
```

## Data Models

### Core Entities

#### Manuscripts
```python
# backend/apps/manuscripts/models.py

class Manuscript(models.Model):
    """Core manuscript entity"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    # Identification
    shelfmark = models.CharField(max_length=255, db_index=True)
    repository = models.CharField(max_length=255)
    collection = models.CharField(max_length=255, blank=True)
    alternative_names = models.JSONField(default=list)

    # Physical description
    material = models.CharField(max_length=50)  # parchment, paper, etc.
    dimensions = models.JSONField()  # {height: X, width: Y, unit: "mm"}
    folios = models.IntegerField()

    # Dating & provenance
    date_earliest = models.IntegerField(null=True)
    date_latest = models.IntegerField(null=True)
    date_display = models.CharField(max_length=100)
    origin_location = models.CharField(max_length=255, blank=True)
    provenance = models.TextField(blank=True)

    # Content
    language = models.CharField(max_length=50)
    script = models.CharField(max_length=50)
    content_summary = models.TextField()

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)

    # Bibliography
    bibliography = models.JSONField(default=list)

    class Meta:
        ordering = ['shelfmark']
        indexes = [
            models.Index(fields=['repository', 'shelfmark']),
            models.Index(fields=['date_earliest', 'date_latest']),
        ]


class Surrogate(models.Model):
    """Photos, prints, and other representations of manuscripts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE,
                                   related_name='surrogates')

    # Type
    SURROGATE_TYPES = [
        ('photo', 'Photograph'),
        ('scan', 'Digital Scan'),
        ('print', 'Printed Edition'),
        ('facsimile', 'Facsimile'),
        ('derivative', 'Derivative Work'),
    ]
    surrogate_type = models.CharField(max_length=20, choices=SURROGATE_TYPES)

    # Identification
    folio_number = models.CharField(max_length=20)  # "12r", "45v", etc.
    sequence_number = models.IntegerField(default=1)

    # Image storage
    image_url = models.URLField()  # S3/MinIO path
    thumbnail_url = models.URLField(blank=True)
    iiif_manifest = models.URLField(blank=True)  # IIIF manifest URL

    # Technical metadata
    width = models.IntegerField()
    height = models.IntegerField()
    dpi = models.IntegerField(null=True)
    file_format = models.CharField(max_length=10)
    file_size = models.BigIntegerField()

    # Capture information
    capture_date = models.DateField(null=True)
    photographer = models.CharField(max_length=255, blank=True)
    copyright_holder = models.CharField(max_length=255, blank=True)
    license = models.CharField(max_length=100, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['folio_number', 'sequence_number']
        unique_together = [['manuscript', 'folio_number', 'sequence_number']]
```

#### Heraldry
```python
# backend/apps/heraldry/models.py

class Arms(models.Model):
    """A coat of arms appearance in a manuscript"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    # Location
    manuscript = models.ForeignKey('manuscripts.Manuscript',
                                   on_delete=models.CASCADE,
                                   related_name='arms')
    surrogate = models.ForeignKey('manuscripts.Surrogate',
                                  on_delete=models.CASCADE,
                                  related_name='arms')

    # Subject
    bearer_name = models.CharField(max_length=255, db_index=True)
    bearer_title = models.CharField(max_length=255, blank=True)
    bearer_dates = models.CharField(max_length=100, blank=True)

    # Blazon (textual description)
    blazon_text = models.TextField()
    blazon_language = models.CharField(max_length=10, default='en')
    blazon_normalized = models.TextField()  # Standardized form

    # Parsed heraldic structure
    field_tincture = models.CharField(max_length=50)
    charges = models.JSONField(default=list)  # [{type, tincture, position, ...}]
    ordinaries = models.JSONField(default=list)
    divisions = models.JSONField(default=dict)

    # Visual markup (coordinates on image)
    shield_outline = models.JSONField()  # polygon points
    charge_regions = models.JSONField(default=list)  # regions for each charge

    # Comparison & similarity
    structural_hash = models.CharField(max_length=64, db_index=True)
    visual_embedding = models.BinaryField(null=True)  # for similarity search

    # Attribution & notes
    attribution_confidence = models.CharField(max_length=20)
    notes = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)

    class Meta:
        ordering = ['bearer_name']
        indexes = [
            models.Index(fields=['bearer_name']),
            models.Index(fields=['field_tincture']),
            models.Index(fields=['structural_hash']),
        ]
        verbose_name_plural = 'Arms'


class Tincture(models.Model):
    """Heraldic colors and metals"""
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20)  # metal, colour, fur, stain

    # Visual representation
    hex_color = models.CharField(max_length=7)
    pattern_svg = models.TextField(blank=True)  # For furs

    # Linguistic
    name_french = models.CharField(max_length=50)
    name_latin = models.CharField(max_length=50, blank=True)

    # Heraldic rules
    is_metal = models.BooleanField(default=False)
    is_colour = models.BooleanField(default=False)


class Charge(models.Model):
    """Heraldic charges (lions, eagles, crosses, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)  # beast, bird, celestial, etc.

    # Classification
    parent_category = models.ForeignKey('self', null=True, blank=True,
                                       on_delete=models.SET_NULL)

    # Visual representation
    svg_template = models.TextField(blank=True)

    # Variations
    common_attitudes = models.JSONField(default=list)  # rampant, passant, etc.
    common_attributes = models.JSONField(default=list)  # armed, langued, etc.

    # Search
    aliases = models.JSONField(default=list)
    search_vector = models.GeneratedField(
        expression=SearchVector('name', 'category'),
        output_field=models.TextField(),
        db_persist=True
    )
```

#### Recession (Manuscript Relationships)
```python
# backend/apps/recession/models.py

class ManuscriptRelationship(models.Model):
    """Tracks copying and derivation relationships between manuscripts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    # Relationship
    source = models.ForeignKey('manuscripts.Manuscript',
                              on_delete=models.CASCADE,
                              related_name='derived_from_relationships')
    target = models.ForeignKey('manuscripts.Manuscript',
                              on_delete=models.CASCADE,
                              related_name='source_for_relationships')

    # Type of relationship
    RELATIONSHIP_TYPES = [
        ('copy', 'Direct Copy'),
        ('derived', 'Derived From'),
        ('exemplar', 'Exemplar Of'),
        ('variant', 'Variant Of'),
        ('excerpt', 'Excerpt From'),
        ('compilation', 'Compiled From'),
    ]
    relationship_type = models.CharField(max_length=20,
                                        choices=RELATIONSHIP_TYPES)

    # Evidence
    confidence = models.CharField(max_length=20,
                                 choices=[
                                     ('certain', 'Certain'),
                                     ('probable', 'Probable'),
                                     ('possible', 'Possible'),
                                     ('speculative', 'Speculative'),
                                 ])
    evidence = models.TextField()

    # Scope
    affects_folios = models.CharField(max_length=255, blank=True)
    affects_content = models.CharField(max_length=255, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)

    class Meta:
        unique_together = [['source', 'target', 'relationship_type']]
        indexes = [
            models.Index(fields=['source', 'relationship_type']),
            models.Index(fields=['target', 'relationship_type']),
        ]


class RecessionTree(models.Model):
    """A complete stemma/family tree of manuscript relationships"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()

    # The manuscripts included in this tree
    manuscripts = models.ManyToManyField('manuscripts.Manuscript')

    # Tree structure (as JSON for visualization)
    tree_structure = models.JSONField()

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)
```

#### Transcription
```python
# backend/apps/transcription/models.py

class Transcription(models.Model):
    """Text transcription from a manuscript surrogate"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    # Location
    surrogate = models.ForeignKey('manuscripts.Surrogate',
                                 on_delete=models.CASCADE,
                                 related_name='transcriptions')

    # Region on the page
    region_coordinates = models.JSONField()  # {x, y, width, height}

    # Text content
    text = models.TextField()
    normalized_text = models.TextField()  # expanded abbreviations, etc.

    # Transcription method
    TRANSCRIPTION_TYPES = [
        ('diplomatic', 'Diplomatic'),
        ('semi-diplomatic', 'Semi-diplomatic'),
        ('normalized', 'Normalized'),
        ('translation', 'Translation'),
    ]
    transcription_type = models.CharField(max_length=20,
                                         choices=TRANSCRIPTION_TYPES)

    # Language & script
    language = models.CharField(max_length=50)
    script = models.CharField(max_length=50)

    # Editorial markers
    uncertain_readings = models.JSONField(default=list)
    editorial_notes = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transcribed_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)

    # Search
    search_vector = models.GeneratedField(
        expression=SearchVector('text', 'normalized_text'),
        output_field=models.TextField(),
        db_persist=True
    )
```

#### Markup & Annotations
```python
# backend/apps/markup/models.py

class Annotation(models.Model):
    """General-purpose annotation on a surrogate"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    # Target
    surrogate = models.ForeignKey('manuscripts.Surrogate',
                                 on_delete=models.CASCADE,
                                 related_name='annotations')

    # Geometry
    ANNOTATION_TYPES = [
        ('point', 'Point'),
        ('rect', 'Rectangle'),
        ('polygon', 'Polygon'),
        ('circle', 'Circle'),
    ]
    annotation_type = models.CharField(max_length=20,
                                      choices=ANNOTATION_TYPES)
    coordinates = models.JSONField()

    # Content
    label = models.CharField(max_length=255)
    category = models.CharField(max_length=50, db_index=True)
    description = models.TextField(blank=True)

    # Optional links
    related_arms = models.ForeignKey('heraldry.Arms', null=True, blank=True,
                                    on_delete=models.SET_NULL)
    related_transcription = models.ForeignKey('transcription.Transcription',
                                             null=True, blank=True,
                                             on_delete=models.SET_NULL)

    # Tags
    tags = models.JSONField(default=list)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)
```

#### Paleography (FastAPI)
```python
# paleography/app/models.py (Pydantic models for API)

class LineUpload(BaseModel):
    ms_id: str
    folio: str
    line_no: int
    script_hint: Optional[str] = None
    date_hint: Optional[int] = None


class EmbeddingRequest(BaseModel):
    line_ids: List[str]
    model: str = "dinov2-base"


class ComparisonRequest(BaseModel):
    line_ids: List[str]
    metric: str = "cosine"
    topk: int = 5


class ClusterRequest(BaseModel):
    line_ids: List[str]
    method: str = "agg"  # agg or dbscan
    params: Dict[str, Any] = {}


class ScribeSimilarityReport(BaseModel):
    job_id: str
    manuscript_ids: List[str]
    total_lines: int
    clusters: List[Dict[str, Any]]
    distance_matrix_summary: Dict[str, float]
    nearest_neighbors: List[Dict[str, Any]]
    created_at: datetime
```

## API Design

### Core API (Django REST Framework)

#### Manuscript Endpoints
```
GET    /api/v1/manuscripts/              # List manuscripts
POST   /api/v1/manuscripts/              # Create manuscript
GET    /api/v1/manuscripts/{id}/         # Get manuscript detail
PATCH  /api/v1/manuscripts/{id}/         # Update manuscript
DELETE /api/v1/manuscripts/{id}/         # Delete manuscript

GET    /api/v1/manuscripts/{id}/surrogates/        # List surrogates
POST   /api/v1/manuscripts/{id}/surrogates/        # Upload surrogate
GET    /api/v1/surrogates/{id}/                    # Get surrogate
DELETE /api/v1/surrogates/{id}/                    # Delete surrogate

GET    /api/v1/manuscripts/{id}/relationships/     # Get relationships
POST   /api/v1/manuscripts/{id}/relationships/     # Create relationship
GET    /api/v1/recession-trees/                    # List stemma trees
POST   /api/v1/recession-trees/                    # Create stemma tree
```

#### Heraldry Endpoints
```
GET    /api/v1/arms/                     # List arms
POST   /api/v1/arms/                     # Create arms entry
GET    /api/v1/arms/{id}/                # Get arms detail
PATCH  /api/v1/arms/{id}/                # Update arms
DELETE /api/v1/arms/{id}/                # Delete arms

POST   /api/v1/arms/compare/             # Compare multiple arms
GET    /api/v1/arms/search/              # Search arms by criteria
POST   /api/v1/arms/{id}/similar/        # Find similar arms

GET    /api/v1/tinctures/                # List tinctures
GET    /api/v1/charges/                  # List charges
GET    /api/v1/charges/search/           # Search charges

POST   /api/v1/blazons/parse/            # Parse blazon text
POST   /api/v1/blazons/generate/         # Generate blazon from structure
POST   /api/v1/blazons/validate/         # Validate blazon syntax
```

#### Transcription Endpoints
```
GET    /api/v1/transcriptions/           # List transcriptions
POST   /api/v1/transcriptions/           # Create transcription
GET    /api/v1/transcriptions/{id}/      # Get transcription
PATCH  /api/v1/transcriptions/{id}/      # Update transcription
DELETE /api/v1/transcriptions/{id}/      # Delete transcription
```

#### Annotation Endpoints
```
GET    /api/v1/annotations/              # List annotations
POST   /api/v1/annotations/              # Create annotation
GET    /api/v1/annotations/{id}/         # Get annotation
PATCH  /api/v1/annotations/{id}/         # Update annotation
DELETE /api/v1/annotations/{id}/         # Delete annotation

GET    /api/v1/surrogates/{id}/annotations/  # Get all annotations for surrogate
```

#### Search Endpoints
```
POST   /api/v1/search/                   # Universal search
POST   /api/v1/search/manuscripts/       # Manuscript search
POST   /api/v1/search/arms/              # Heraldic search
POST   /api/v1/search/transcriptions/    # Text search

Example heraldic search request:
{
  "field_tincture": "gules",
  "charges": ["lion", "eagle"],
  "bearer_name": "Percy",
  "date_range": [1300, 1500],
  "manuscripts": ["uuid1", "uuid2"]
}
```

### Paleography API (FastAPI)

```
POST   /lines                            # Upload line image
POST   /embed                            # Compute embeddings
POST   /compare                          # Compare lines
POST   /cluster                          # Cluster by similarity
GET    /report/{job_id}                  # Get analysis report

POST   /manuscripts/{ms_id}/analyze      # Analyze all lines in MS
GET    /manuscripts/compare              # Compare scribes across MSS
```

## Feature Details

### 1. Manuscript Viewing & Navigation

**Key Features:**
- High-resolution image viewing with zoom/pan
- IIIF protocol support for interoperability
- Side-by-side surrogate comparison
- Folio navigation with thumbnails
- Lightbox mode for focused viewing

**Components:**
- `ManuscriptViewer` - Main viewer component with OpenSeadragon
- `FolioNavigator` - Thumbnail strip and page selector
- `SurrogateSelector` - Toggle between different surrogates
- `ZoomControls` - Zoom, pan, rotate controls

### 2. Heraldic Markup

**Key Features:**
- Draw shield outlines on images
- Mark individual charges and ordinaries
- Tag tinctures for each element
- Link markup to blazon descriptions
- Validate against heraldic rules

**Heraldic Rules Engine:**
- Tincture on tincture violations (metal on metal, colour on colour)
- Proper positioning and orientation rules
- Cadency markers validation
- Marshalling rules for quartered arms

**Components:**
- `HeraldryCanvas` - Fabric.js canvas for drawing
- `ShieldDrawer` - Tool for outlining shields
- `ChargeMarker` - Mark and label charges
- `TinctureSelector` - Visual tincture picker
- `BlazonEditor` - Rich text editor with heraldic autocomplete

### 3. Arms Comparison

**Key Features:**
- Multi-panel comparison view
- Visual diff highlighting
- Structural comparison (charges, tinctures)
- Similarity scoring
- Export comparison reports

**Comparison Metrics:**
- Exact match (same bearer, same blazon)
- Structural similarity (Jaccard index on charges)
- Visual similarity (CNN embeddings)
- Temporal proximity (date ranges)

**Components:**
- `ArmsComparison` - Main comparison interface
- `ComparisonPanel` - Individual arms panel
- `SimilarityMatrix` - Heatmap of similarities
- `DifferenceHighlighter` - Visual diff overlay

### 4. Heraldic Search

**Search Dimensions:**
- **By Bearer**: Name, title, dates
- **By Blazon**: Text search on descriptions
- **By Structure**: Field tincture, charges, ordinaries
- **By Rules**: Find rule violations
- **By Similarity**: Visual or structural similarity
- **By Manuscript**: Limit to specific MSS or date ranges

**Search Query Builder:**
```typescript
interface HeraldrySearchQuery {
  bearer?: {
    name?: string;
    title?: string;
    dateRange?: [number, number];
  };
  blazon?: {
    text?: string;
    language?: string;
  };
  structure?: {
    fieldTincture?: string[];
    charges?: string[];
    ordinaries?: string[];
    divisions?: string;
  };
  rules?: {
    findViolations?: boolean;
    violationType?: string[];
  };
  manuscripts?: string[];  // UUIDs
  similarity?: {
    referenceArmsId: string;
    threshold: number;
    metric: 'visual' | 'structural';
  };
}
```

**Components:**
- `HeraldrySearchBuilder` - Visual query builder
- `SearchFilters` - Faceted filters
- `SearchResults` - Grid/list of results
- `SavedSearches` - Save and manage queries

### 5. Recession Tracking

**Key Features:**
- Build manuscript family trees
- Visualize relationships
- Evidence documentation
- Confidence levels
- Export stemmata

**Visualization:**
- Interactive tree diagram (D3.js or Cytoscape.js)
- Temporal axis for chronological view
- Highlight paths between manuscripts
- Color-code by relationship type

**Components:**
- `RecessionTreeBuilder` - Interactive tree editor
- `RecessionVisualization` - D3-based stemma viewer
- `RelationshipEditor` - Create/edit relationships
- `EvidencePanel` - Document supporting evidence

### 6. Paleography Analysis

**Workflow:**
1. Upload line images from multiple manuscripts
2. System computes DINOv2 embeddings
3. Calculate pairwise similarities
4. Cluster similar hands
5. Visualize results (heatmap, dendrogram, UMAP)
6. Export findings

**Analysis Types:**
- **Intra-manuscript**: Are all hands in MS X the same?
- **Inter-manuscript**: Do MS X and MS Y share a scribe?
- **Workshop detection**: Find clustered groups across MSS
- **Temporal analysis**: Track scribal style evolution

**Components:**
- `PaleographyUploader` - Batch line upload
- `ScribeAnalysis` - Analysis configuration
- `SimilarityHeatmap` - Visual similarity matrix
- `ClusterVisualization` - Dendrogram and UMAP plots
- `ScribeProfile` - View all lines attributed to a hand

### 7. Transcription

**Key Features:**
- Draw text regions on images
- Multi-level transcription (diplomatic, normalized)
- Abbreviation expansion
- Uncertainty marking
- Full-text search

**Editor Features:**
- Special character palette (ꝑ, ꝓ, ꝗ, etc.)
- Abbreviation helper
- Parallel viewing (image + text)
- TEI XML export option

**Components:**
- `TranscriptionEditor` - Rich text editor
- `RegionSelector` - Draw text regions
- `SpecialCharacters` - Character picker
- `AbbreviationExpander` - Abbreviation tool

## Development Roadmap

### Phase 1: Foundation (Weeks 1-4)
**Goal:** Basic infrastructure and core manuscript management

1. **Infrastructure Setup**
   - Initialize monorepo structure
   - Docker Compose for local development
   - PostgreSQL + Redis + MinIO setup
   - CI/CD pipeline (GitHub Actions)

2. **Backend Core**
   - Django project setup with DRF
   - Manuscript and Surrogate models
   - Basic CRUD endpoints
   - Object storage integration (MinIO)
   - Authentication & permissions

3. **Frontend Core**
   - Next.js project setup
   - Layout and navigation
   - Authentication flow
   - API client setup (React Query)
   - Basic manuscript list/detail views

**Deliverables:**
- Running development environment
- Can create/view manuscripts
- Can upload surrogate images
- Basic user authentication

### Phase 2: Viewing & Markup (Weeks 5-8)
**Goal:** Manuscript viewing and basic annotation

1. **Image Viewer**
   - OpenSeadragon integration
   - IIIF manifest support
   - Zoom/pan controls
   - Folio navigation

2. **Annotation System**
   - Fabric.js canvas integration
   - Draw rectangles and polygons
   - Annotation CRUD operations
   - Annotation categories

3. **UI Polish**
   - Responsive design
   - Tailwind styling
   - Loading states
   - Error handling

**Deliverables:**
- High-quality image viewer
- Can draw and save annotations
- Clean, professional UI

### Phase 3: Heraldry Core (Weeks 9-12)
**Goal:** Heraldic data management and markup

1. **Heraldic Models**
   - Arms, Tincture, Charge models
   - Blazon parser (basic)
   - Heraldic rules engine

2. **Heraldic Markup**
   - Shield drawing tools
   - Charge marking
   - Tincture selection
   - Link markup to blazons

3. **Heraldic Data Entry**
   - Arms creation forms
   - Blazon editor with autocomplete
   - Tincture and charge libraries

**Deliverables:**
- Can create arms entries
- Can markup shields on images
- Basic blazon support
- Tincture validation

### Phase 4: Search & Comparison (Weeks 13-16)
**Goal:** Search functionality and arms comparison

1. **Search Implementation**
   - PostgreSQL full-text search
   - Search query builder
   - Faceted filtering
   - Search result views

2. **Arms Comparison**
   - Multi-panel comparison view
   - Structural similarity metrics
   - Comparison reports

3. **Advanced Blazon**
   - Enhanced blazon parser
   - Blazon validation
   - Blazon generation from structure

**Deliverables:**
- Full heraldic search
- Side-by-side arms comparison
- Similarity scoring
- Export capabilities

### Phase 5: Recession & Relationships (Weeks 17-20)
**Goal:** Manuscript relationship tracking

1. **Relationship Models**
   - ManuscriptRelationship model
   - RecessionTree model
   - Evidence documentation

2. **Tree Visualization**
   - D3.js stemma visualization
   - Interactive tree builder
   - Path highlighting

3. **Relationship Management**
   - Create/edit relationships
   - Confidence levels
   - Evidence linking

**Deliverables:**
- Can define manuscript relationships
- Interactive stemma visualization
- Export stemma diagrams

### Phase 6: Transcription (Weeks 21-23)
**Goal:** Text transcription functionality

1. **Transcription Models**
   - Transcription model
   - Region selection

2. **Transcription Editor**
   - Rich text editor
   - Special characters
   - Abbreviation tools

3. **Search Integration**
   - Full-text search on transcriptions
   - Link transcriptions to other entities

**Deliverables:**
- Can transcribe text from images
- Special character support
- Searchable transcriptions

### Phase 7: Paleography Service (Weeks 24-28)
**Goal:** Scribe similarity analysis

1. **FastAPI Service**
   - Implement provided FastAPI service
   - DINOv2 model integration
   - Redis caching
   - MinIO storage for line images

2. **Integration**
   - Connect FastAPI to main app
   - API client in Next.js
   - Shared authentication

3. **Paleography UI**
   - Line upload interface
   - Analysis configuration
   - Similarity visualization
   - Cluster explorer

**Deliverables:**
- Working paleography microservice
- Can analyze scribal hands
- Visual similarity reports
- Clustering results

### Phase 8: Polish & Documentation (Weeks 29-32)
**Goal:** Production readiness

1. **Performance Optimization**
   - Database query optimization
   - Image loading optimization
   - Caching strategies
   - Lazy loading

2. **Testing**
   - Unit tests (Django, FastAPI)
   - Integration tests
   - E2E tests (Playwright)
   - Load testing

3. **Documentation**
   - API documentation (OpenAPI)
   - User guide
   - Development guide
   - Deployment guide

4. **Deployment**
   - Production Docker setup
   - Kubernetes manifests (optional)
   - Monitoring setup
   - Backup procedures

**Deliverables:**
- Comprehensive test coverage
- Complete documentation
- Production deployment
- Monitoring and logging

## UI/UX Design Principles

### Style Guide

**Visual Style:**
- **Theme**: Elegant, scholarly, with medieval touches
- **Colors**:
  - Primary: Deep blue (#1e3a8a) - evokes heraldic azure
  - Secondary: Rich red (#991b1b) - evokes heraldic gules
  - Accent: Gold (#d97706) - evokes heraldic or
  - Neutral: Warm grays with parchment tones
- **Typography**:
  - Headers: Playfair Display or Lora (serif, elegant)
  - Body: Inter or Source Sans Pro (sans-serif, readable)
  - Monospace: JetBrains Mono (for transcriptions)

**Component Style:**
- Generous whitespace
- Subtle shadows and borders
- Smooth transitions
- High-contrast for accessibility
- WCAG AA compliance minimum

### Key UI Patterns

1. **Master-Detail Layout**
   - Left sidebar: List/navigation
   - Main content: Detail view
   - Right sidebar: Metadata/tools

2. **Multi-Panel Comparison**
   - 2-4 synchronized panels
   - Linked scrolling/zooming
   - Difference highlighting

3. **Canvas-Based Annotation**
   - Non-modal tools
   - Persistent toolbar
   - Keyboard shortcuts
   - Undo/redo

4. **Guided Workflows**
   - Step-by-step wizards for complex tasks
   - Progress indicators
   - Context-sensitive help

### Responsive Design

- **Desktop (1280px+)**: Full multi-column layouts
- **Tablet (768-1279px)**: Collapsible sidebars, stacked panels
- **Mobile (< 768px)**: Single column, bottom navigation

## Security Considerations

1. **Authentication & Authorization**
   - JWT-based authentication
   - Role-based access control (RBAC)
   - Resource-level permissions
   - API rate limiting

2. **Data Protection**
   - Encryption at rest (PostgreSQL TDE)
   - Encryption in transit (TLS)
   - Secure object storage
   - Regular backups

3. **Input Validation**
   - Sanitize all user inputs
   - Validate file uploads (type, size)
   - Parameterized queries (ORM)
   - CSRF protection

4. **API Security**
   - CORS configuration
   - Rate limiting
   - API versioning
   - Request validation (Pydantic)

## Performance Considerations

1. **Database**
   - Proper indexing
   - Connection pooling
   - Query optimization
   - Materialized views for complex queries

2. **Images**
   - Progressive loading
   - Thumbnail generation
   - CDN for static assets
   - IIIF tiles for large images

3. **Caching**
   - Redis for session and API caching
   - Browser caching headers
   - Service worker for offline support

4. **API**
   - Pagination for lists
   - Field selection (sparse fieldsets)
   - Batch operations
   - Background tasks for heavy operations

## Testing Strategy

1. **Unit Tests**
   - Django models and views (pytest)
   - FastAPI endpoints (pytest)
   - React components (Vitest + Testing Library)
   - Utility functions

2. **Integration Tests**
   - API endpoint workflows
   - Database operations
   - External service mocks

3. **E2E Tests**
   - Critical user journeys (Playwright)
   - Cross-browser testing
   - Accessibility testing

4. **Performance Tests**
   - Load testing (Locust)
   - Database query profiling
   - Frontend performance (Lighthouse)

## Deployment Architecture

### Development
```
Docker Compose:
- Next.js (dev server)
- Django (runserver)
- FastAPI (uvicorn --reload)
- PostgreSQL
- Redis
- MinIO
```

### Production
```
Kubernetes/Docker Compose:
- Next.js (static export + Node server)
- Django (Gunicorn + multiple workers)
- FastAPI (Uvicorn + multiple workers)
- PostgreSQL (managed service or HA cluster)
- Redis (managed service or cluster)
- S3 or MinIO cluster
- Nginx (reverse proxy + static files)
- Certbot (SSL certificates)
```

## Future Enhancements

1. **Advanced Paleography**
   - Letter-level analysis
   - Glyph detection and comparison
   - Fine-tuned models on medieval scripts

2. **Collaborative Features**
   - Real-time collaboration
   - Comments and discussions
   - Change tracking and versioning

3. **AI Assistance**
   - Automatic charge detection
   - Blazon generation from images
   - Transcription assistance (HTR)

4. **Export & Publishing**
   - PDF reports
   - TEI XML export
   - IIIF manifest generation
   - Data dumps for research

5. **Integrations**
   - External manuscript databases
   - Linked Open Data (LOD)
   - Citation management (Zotero)

6. **Mobile Apps**
   - Native iOS/Android apps
   - Field photography tools
   - Offline support

## Conclusion

Herald represents a comprehensive platform for heraldic scholarship, combining traditional manuscript studies with modern paleographic analysis. The architecture is designed to be:

- **Scalable**: Microservices can scale independently
- **Maintainable**: Clear separation of concerns
- **Extensible**: Easy to add new features
- **User-friendly**: Elegant UI guiding users through complex workflows
- **Research-grade**: Rigorous data models and scholarly features

The phased development approach allows for incremental delivery of value while building toward the complete vision.

# Paleography Service - Technical Specification

## Overview

The paleography service is a specialized microservice for analyzing scribal hands in medieval manuscripts using computer vision and machine learning. It computes visual embeddings of handwriting samples and identifies similarities that may indicate shared scribes, scribal schools, or workshops.

## Purpose

Given images of individual text lines from multiple manuscripts, the service:
- Computes style embeddings using self-supervised vision models
- Quantifies similarity between different hands
- Clusters similar writing styles
- Generates comparative visualizations

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              FastAPI Application                     │
│  ┌──────────┐  ┌──────────┐  ┌────────────────┐   │
│  │ Upload   │  │ Embed    │  │ Compare/Cluster│   │
│  │ Endpoint │  │ Endpoint │  │ Endpoints      │   │
│  └────┬─────┘  └────┬─────┘  └────────┬───────┘   │
│       │             │                  │            │
│       ▼             ▼                  ▼            │
│  ┌──────────────────────────────────────────────┐  │
│  │         Vision Processing Layer              │  │
│  │  - Preprocessing (deskew, CLAHE, resize)     │  │
│  │  - DINOv2 embedding extraction               │  │
│  │  - Distance matrix computation               │  │
│  │  - Clustering (Agglomerative, DBSCAN)        │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐    ┌─────────┐    ┌──────────┐
   │  MinIO  │    │  Redis  │    │Postgres  │
   │(Images) │    │(Embed.) │    │(Metadata)│
   └─────────┘    └─────────┘    └──────────┘
```

## Data Model

### Lines Table (PostgreSQL)

Stores metadata about each line image:

```sql
CREATE TABLE lines (
  id UUID PRIMARY KEY,
  ms_id TEXT NOT NULL,           -- Manuscript identifier
  folio TEXT NOT NULL,            -- Folio reference (e.g., "12r", "45v")
  line_no INT NOT NULL,           -- Line number on folio
  img_uri TEXT NOT NULL,          -- S3/MinIO URI
  width INT,                      -- Image width in pixels
  height INT,                     -- Image height in pixels
  dpi INT,                        -- Dots per inch (if known)
  script_hint TEXT,               -- Script type (e.g., "gothic", "carolingian")
  date_hint INT,                  -- Approximate date
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_lines_ms_id ON lines(ms_id);
CREATE INDEX idx_lines_folio ON lines(ms_id, folio);
```

### Embeddings (Redis)

For fast access, embeddings are stored in Redis:

```
Key: "emb:{line_id}"
Value: Binary-serialized float32 array (768 or 1024 dimensions)
TTL: Optional (e.g., 7 days for cache eviction)
```

Metadata about embeddings can optionally be persisted to PostgreSQL:

```sql
CREATE TABLE embeddings (
  line_id UUID REFERENCES lines(id) ON DELETE CASCADE,
  vector BYTEA NOT NULL,          -- Or use pgvector extension
  model TEXT NOT NULL,            -- e.g., "dinov2-base"
  norm BOOLEAN DEFAULT true,      -- Whether vector is normalized
  created_at TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (line_id, model)
);
```

### Comparison Jobs (Optional - PostgreSQL)

For persisting analysis results:

```sql
CREATE TABLE comparisons (
  job_id UUID PRIMARY KEY,
  line_ids UUID[] NOT NULL,       -- Array of line IDs analyzed
  distance_matrix_uri TEXT,       -- S3 URI to numpy array
  cluster_labels JSONB,           -- [{line_id, label}, ...]
  umap_2d JSONB,                  -- [{line_id, x, y}, ...]
  method TEXT,                    -- "agg", "dbscan", etc.
  params JSONB,                   -- Method parameters
  created_at TIMESTAMPTZ DEFAULT now()
);
```

## API Endpoints

### POST /lines - Upload Line Image

Uploads a cropped line image with metadata.

**Request:**
```http
POST /lines
Content-Type: multipart/form-data

image: <binary image data>
ms_id: "MS_Bodley_123"
folio: "45r"
line_no: 12
script_hint: "gothic" (optional)
date_hint: 1450 (optional)
```

**Response:**
```json
{
  "line_id": "550e8400-e29b-41d4-a716-446655440000",
  "img_uri": "s3://scribe-sim/lines/550e8400-e29b-41d4-a716-446655440000.png",
  "width": 2048,
  "height": 224
}
```

### POST /embed - Compute Embeddings

Computes DINOv2 embeddings for specified line images.

**Request:**
```json
{
  "line_ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
  ],
  "model": "dinov2-base"  // optional
}
```

**Response:**
```json
{
  "embeddings": [
    {
      "line_id": "550e8400-e29b-41d4-a716-446655440000",
      "dim": 768
    },
    {
      "line_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
      "dim": 768
    }
  ]
}
```

### POST /compare - Compare Lines

Computes pairwise distances and finds nearest neighbors.

**Request:**
```json
{
  "line_ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
    "7c9e6679-7425-40de-944b-e07fc1f90ae7"
  ],
  "metric": "cosine",  // default
  "topk": 5            // number of nearest neighbors
}
```

**Response:**
```json
{
  "order": ["550e8400-...", "6ba7b810-...", "7c9e6679-..."],
  "D": [
    [0.0, 0.234, 0.567],
    [0.234, 0.0, 0.432],
    [0.567, 0.432, 0.0]
  ],
  "nearest": [
    {
      "line_id": "550e8400-...",
      "topk": [
        {"line_id": "6ba7b810-...", "dist": 0.234},
        {"line_id": "7c9e6679-...", "dist": 0.567}
      ]
    },
    // ... more entries
  ]
}
```

### POST /cluster - Cluster by Similarity

Groups lines into clusters based on visual similarity.

**Request:**
```json
{
  "line_ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
    // ... more IDs
  ],
  "method": "agg",  // "agg" or "dbscan"
  "params": {
    "distance_threshold": 0.35,  // for agglomerative
    "linkage": "average"
    // OR for DBSCAN:
    // "eps": 0.3,
    // "min_samples": 2
  }
}
```

**Response:**
```json
{
  "labels": [
    {"line_id": "550e8400-...", "label": 0},
    {"line_id": "6ba7b810-...", "label": 0},
    {"line_id": "7c9e6679-...", "label": 1}
  ],
  "k": 2  // number of clusters (for agg)
}
```

### GET /report/{job_id} - Get Analysis Report

Returns a comprehensive analysis report (if jobs are persisted).

**Response:**
```json
{
  "job_id": "abc123...",
  "manuscript_ids": ["MS_Bodley_123", "MS_Digby_456"],
  "total_lines": 45,
  "clusters": [
    {
      "label": 0,
      "size": 23,
      "manuscripts": ["MS_Bodley_123"],
      "avg_distance": 0.15
    },
    {
      "label": 1,
      "size": 22,
      "manuscripts": ["MS_Digby_456"],
      "avg_distance": 0.12
    }
  ],
  "distance_matrix_summary": {
    "min": 0.0,
    "max": 0.85,
    "mean": 0.42,
    "std": 0.18
  },
  "created_at": "2025-11-12T10:30:00Z"
}
```

## Vision Processing Pipeline

### 1. Preprocessing

Transform input images to standardize for embedding extraction:

```python
def preprocess_pil(im: Image.Image) -> Image.Image:
    """
    Preprocessing pipeline:
    1. Convert to grayscale
    2. Gaussian blur (noise reduction)
    3. Deskew (correct rotation)
    4. CLAHE (contrast enhancement)
    5. Otsu thresholding (binarization)
    6. Padding and resize
    """
    # Convert to grayscale
    gray = np.array(im.convert("L"))

    # Denoise
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Deskew using minAreaRect
    coords = np.column_stack(np.where(gray < 250))
    if coords.size > 0:
        angle = cv2.minAreaRect(coords.astype(np.float32))[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = gray.shape[:2]
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
        gray = cv2.warpAffine(gray, M, (w, h),
                             flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)

    # CLAHE for contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Binarize
    _, gray = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert back to PIL
    pil = Image.fromarray(gray)

    # Add padding
    pil = ImageOps.expand(pil, border=8, fill=255)

    # Resize to model input size
    pil = pil.resize((448, 448), Image.LANCZOS)

    return pil.convert("RGB")
```

### 2. Embedding Extraction

Use DINOv2 to extract visual features:

```python
def embed_image(pil_im: Image.Image) -> np.ndarray:
    """
    Extract normalized embedding using DINOv2.
    Returns: float32 array of shape (768,) for base model
    """
    # Preprocess for DINOv2
    inputs = image_processor(images=pil_im, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Forward pass
    with torch.no_grad():
        outputs = model(**inputs)
        # Use mean of hidden states as embedding
        hidden_states = outputs.last_hidden_state  # shape: [1, num_patches, dim]
        embedding = hidden_states.mean(dim=1)      # shape: [1, dim]

    # Convert to numpy and normalize
    vec = embedding[0].float().cpu().numpy()
    vec = vec / np.linalg.norm(vec)

    return vec.astype("float32")
```

### 3. Distance Computation

Compute pairwise cosine distances:

```python
def pairwise_cosine(embeddings: List[np.ndarray]) -> np.ndarray:
    """
    Compute pairwise cosine distance matrix.

    Args:
        embeddings: List of normalized embedding vectors

    Returns:
        Distance matrix D where D[i,j] = cosine_distance(emb[i], emb[j])
        Range: [0, 2], where 0 = identical, 1 = orthogonal, 2 = opposite
    """
    from sklearn.metrics.pairwise import cosine_distances

    V = np.vstack(embeddings)
    D = cosine_distances(V, V)
    return D
```

### 4. Clustering

Cluster embeddings by similarity:

```python
def cluster_agglomerative(D: np.ndarray,
                         distance_threshold: float = 0.35,
                         linkage: str = "average") -> np.ndarray:
    """
    Agglomerative hierarchical clustering.

    Args:
        D: Precomputed distance matrix
        distance_threshold: Threshold for cutting dendrogram
        linkage: "average", "complete", "single"

    Returns:
        Cluster labels array
    """
    from sklearn.cluster import AgglomerativeClustering

    clusterer = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=distance_threshold,
        metric="precomputed",
        linkage=linkage
    )
    labels = clusterer.fit_predict(D)
    return labels


def cluster_dbscan(D: np.ndarray,
                  eps: float = 0.3,
                  min_samples: int = 2) -> np.ndarray:
    """
    DBSCAN clustering.

    Args:
        D: Precomputed distance matrix
        eps: Maximum distance for neighborhood
        min_samples: Minimum samples to form dense region

    Returns:
        Cluster labels array (noise points labeled -1)
    """
    from sklearn.cluster import DBSCAN

    clusterer = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric="precomputed"
    )
    labels = clusterer.fit_predict(D)
    return labels
```

## Vision Model

### DINOv2 (Default)

**Model:** `facebook/dinov2-base` from Hugging Face Transformers

**Why DINOv2?**
- Self-supervised training (no labels needed)
- Strong performance on fine-grained visual tasks
- Robust to domain shifts
- 768-dimensional embeddings (base model)

**Alternatives:**
- `facebook/dinov2-small` - 384 dim, faster but less accurate
- `facebook/dinov2-large` - 1024 dim, more accurate but slower
- `openai/clip-vit-base-patch32` - 512 dim, multimodal (text+image)

### Model Loading

```python
from transformers import AutoImageProcessor, AutoModel

device = "cuda" if torch.cuda.is_available() else "cpu"

image_processor = AutoImageProcessor.from_pretrained("facebook/dinov2-base")
model = AutoModel.from_pretrained("facebook/dinov2-base")
model = model.to(device).eval()
```

## Interpretation Workflow

### Typical Analysis Steps

1. **Data Collection**
   - Upload 20-50 lines per manuscript
   - Ensure consistent quality (DPI, cropping)
   - Include diverse letter forms

2. **Embedding Computation**
   - Batch process all uploaded lines
   - Embeddings cached in Redis for reuse

3. **Pairwise Comparison**
   - Compute distance matrix
   - Identify nearest neighbors for each line
   - Look for cross-manuscript matches

4. **Clustering**
   - Run agglomerative clustering
   - Examine cluster composition:
     - Single-MS clusters → likely single hand
     - Multi-MS clusters → possible shared scribe/workshop

5. **Visualization**
   - Heatmap of distance matrix
   - Dendrogram of hierarchical relationships
   - UMAP 2D projection for intuitive view

6. **Export & Analysis**
   - Export distance matrices as CSV
   - Generate cluster reports
   - Document findings with evidence images

### Interpretation Guidelines

**Distance Thresholds (empirical):**
- `< 0.20`: Very similar, likely same hand
- `0.20-0.35`: Similar, possibly same hand or school
- `0.35-0.50`: Moderate similarity, shared period/region
- `> 0.50`: Different hands

**Important Caveats:**
- Distances are comparative, not absolute
- Use multiple lines to reduce noise
- Consider codicological evidence
- Validate with traditional paleography
- Account for scribal evolution over time

## Extensions & Future Work

### 1. Patch-Level Saliency

Identify which regions drive similarity:

```python
def compute_saliency(image1, image2, embedding1, embedding2):
    """
    Use gradient-based methods to highlight discriminative patches.
    Helps answer: "Which letter forms are most similar?"
    """
    # Compute gradients w.r.t. input
    # Visualize attention maps
    # Overlay on original images
    pass
```

### 2. Letter-Level Analysis

Detect and compare individual glyphs:

```python
def extract_letters(line_image, target_letters=['h', 'g', 's']):
    """
    1. Segment line into characters
    2. Classify characters
    3. Extract embeddings for specific letter types
    4. Compare letter styles across manuscripts
    """
    pass
```

### 3. Fine-Tuning

Improve performance on medieval scripts:

```python
def finetune_dinov2(line_images, labels):
    """
    Fine-tune DINOv2 on labeled medieval script data:
    - Collect known same/different hand pairs
    - Train with contrastive loss
    - Improve embeddings for domain
    """
    pass
```

### 4. Temporal Analysis

Track scribal style evolution:

```python
def temporal_similarity(manuscripts_with_dates):
    """
    1. Cluster hands across dated manuscripts
    2. Fit temporal models to distance changes
    3. Estimate dates for undated MSS
    """
    pass
```

### 5. Multi-Modal Features

Combine vision with text:

```python
def multimodal_embedding(line_image, transcription):
    """
    Combine visual embedding with linguistic features:
    - Spelling patterns
    - Abbreviation preferences
    - Dialect markers
    """
    pass
```

## Deployment Considerations

### GPU Acceleration

For faster embedding extraction:

```dockerfile
# Use CUDA base image
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Install PyTorch with CUDA support
RUN pip install torch==2.4.1+cu121 torchvision==0.19.1+cu121 \
    -f https://download.pytorch.org/whl/torch_stable.html
```

Update `.env`:
```
TORCH_DEVICE=cuda
```

### ONNX Export (Optional)

For CPU-optimized inference:

```python
import torch.onnx

# Export model
torch.onnx.export(
    model,
    dummy_input,
    "dinov2_base.onnx",
    opset_version=14,
    input_names=["pixel_values"],
    output_names=["embeddings"]
)

# Use ONNX Runtime for inference
import onnxruntime as ort
session = ort.InferenceSession("dinov2_base.onnx")
```

### Caching Strategy

Optimize Redis for embeddings:

```python
# Set TTL for embeddings (e.g., 30 days)
redis_client.setex(
    f"emb:{line_id}",
    2592000,  # 30 days in seconds
    embedding.tobytes()
)

# Implement LRU eviction
redis_client.config_set("maxmemory-policy", "allkeys-lru")
redis_client.config_set("maxmemory", "2gb")
```

### Batch Processing

Process multiple embeddings efficiently:

```python
@app.post("/embed-batch")
async def embed_batch(line_ids: List[str], batch_size: int = 16):
    """
    Process embeddings in batches for GPU efficiency.
    """
    results = []
    for i in range(0, len(line_ids), batch_size):
        batch = line_ids[i:i+batch_size]
        # Load images
        images = [load_image(lid) for lid in batch]
        # Batch preprocessing
        inputs = image_processor(images=images, return_tensors="pt").to(device)
        # Batch inference
        with torch.no_grad():
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
        # Cache results
        for lid, emb in zip(batch, embeddings):
            cache_embedding(lid, emb.cpu().numpy())
        results.extend(batch)
    return {"processed": len(results)}
```

## Testing

### Unit Tests

```python
# test_vision.py
def test_preprocessing():
    image = Image.open("test_line.png")
    processed = preprocess_pil(image)
    assert processed.size == (448, 448)
    assert processed.mode == "RGB"


def test_embedding_shape():
    image = Image.open("test_line.png")
    processed = preprocess_pil(image)
    embedding = embed_image(processed)
    assert embedding.shape == (768,)
    assert np.allclose(np.linalg.norm(embedding), 1.0)


def test_distance_matrix():
    emb1 = np.random.randn(768).astype("float32")
    emb1 /= np.linalg.norm(emb1)
    emb2 = np.random.randn(768).astype("float32")
    emb2 /= np.linalg.norm(emb2)

    D = pairwise_cosine([emb1, emb2, emb1])
    assert D.shape == (3, 3)
    assert D[0, 2] < 0.01  # Same embedding
```

### Integration Tests

```python
# test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_line():
    with open("test_line.png", "rb") as f:
        response = client.post(
            "/lines",
            files={"image": f},
            data={"ms_id": "TEST_MS", "folio": "1r", "line_no": 1}
        )
    assert response.status_code == 200
    data = response.json()
    assert "line_id" in data
    assert "img_uri" in data


def test_embed_and_compare():
    # Upload two lines
    line_ids = []
    for i in range(2):
        with open(f"test_line_{i}.png", "rb") as f:
            response = client.post(
                "/lines",
                files={"image": f},
                data={"ms_id": "TEST_MS", "folio": "1r", "line_no": i+1}
            )
        line_ids.append(response.json()["line_id"])

    # Compute embeddings
    response = client.post("/embed", json={"line_ids": line_ids})
    assert response.status_code == 200

    # Compare
    response = client.post("/compare", json={"line_ids": line_ids, "topk": 1})
    assert response.status_code == 200
    data = response.json()
    assert "D" in data
    assert len(data["D"]) == 2
```

## Performance Benchmarks

Typical performance on modern hardware:

**Preprocessing:** ~50ms per line (CPU)
**Embedding (DINOv2-base):**
- CPU: ~500ms per image
- GPU (RTX 3090): ~50ms per image
- Batch of 16 on GPU: ~200ms (~12ms per image)

**Distance matrix (100 lines):**
- Computation: ~50ms
- Storage: 100x100x4 bytes = 40KB

**Clustering (100 lines):**
- Agglomerative: ~100ms
- DBSCAN: ~50ms

**Throughput estimates:**
- Single GPU: ~1000 images/minute
- 4-GPU setup: ~4000 images/minute

## References

- Oquab et al. (2024): "DINOv2: Learning Robust Visual Features without Supervision"
- Radford et al. (2021): "Learning Transferable Visual Models From Natural Language Supervision" (CLIP)
- van der Maaten & Hinton (2008): "Visualizing Data using t-SNE"
- McInnes et al. (2018): "UMAP: Uniform Manifold Approximation and Projection"

---

**Implementation Status:** Specification provided, to be implemented in Phase 7
**Last Updated:** 2025-11-12

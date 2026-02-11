# Testing the Manuscript Viewer

## Prerequisites

1. **Backend server running** on `http://localhost:8000`
2. **Frontend server running** on `http://localhost:3000`
3. **At least one manuscript with surrogates** (images)

## Step-by-Step Testing Guide

### Step 1: Verify Services Are Running

```bash
# Check backend
curl http://localhost:8000/api/v1/manuscripts/manuscripts/ | head -20

# Check frontend (should return HTML)
curl http://localhost:3000 | head -10
```

### Step 2: Access a Manuscript

1. Open your browser and go to: **http://localhost:3000/manuscripts**
2. You should see a list of manuscripts
3. Click on any manuscript to view its details

### Step 3: Access the Viewer

**Option A: From Manuscript List**
- Click on any manuscript card
- On the manuscript detail page, click the **"View Images"** button

**Option B: Direct URL**
- Go to: `http://localhost:3000/manuscripts/{manuscript-id}/viewer`
- Replace `{manuscript-id}` with an actual manuscript UUID

### Step 4: Test Viewer Features

#### Basic Navigation
- ✅ **Zoom**: Use mouse wheel or zoom controls
- ✅ **Pan**: Click and drag to move around
- ✅ **Rotate**: Use rotation control (if available)
- ✅ **Home**: Click home button to reset view
- ✅ **Fullscreen**: Click fullscreen button

#### Folio Navigation
- ✅ **Previous/Next buttons**: Navigate between folios
- ✅ **Thumbnail strip**: Click thumbnails at bottom to jump to specific folio
- ✅ **Current folio indicator**: Shows "Image X of Y" in header

### Step 5: Expected Behavior

**If manuscript has images:**
- Viewer should load with first image
- Navigation controls visible
- Thumbnail strip shows all images
- Can navigate between images smoothly

**If manuscript has no images:**
- Shows message: "No images available for this manuscript"
- Link back to manuscript details page

## Troubleshooting

### Issue: "No images available"
**Solution**: You need to upload images first. See "Creating Test Data" below.

### Issue: Viewer doesn't load
**Check:**
1. Browser console for errors (F12)
2. Network tab for failed requests
3. OpenSeadragon CDN is accessible

### Issue: Images don't display
**Check:**
1. Image URLs are accessible (try opening in new tab)
2. CORS is configured correctly
3. MinIO is running (if using MinIO storage)

### Issue: Navigation doesn't work
**Check:**
1. Multiple surrogates exist for the manuscript
2. Surrogate data includes `image_url` field
3. Browser console for JavaScript errors

## Creating Test Data

### Option 1: Upload via Admin

1. Go to: http://localhost:8000/admin
2. Login with: `admin` / `admin123`
3. Navigate to **Manuscripts** → **Surrogates**
4. Click **"Add Surrogate"**
5. Fill in:
   - Manuscript: Select a manuscript
   - Folio number: e.g., "1r"
   - Image URL: Use a test image URL (e.g., from a public image service)
   - Width/Height: Set appropriate dimensions
   - File format: JPEG
   - File size: Approximate size in bytes
6. Click **Save**

### Option 2: Use API

```bash
# Get a manuscript ID first
MANUSCRIPT_ID=$(curl -s http://localhost:8000/api/v1/manuscripts/manuscripts/ | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['results'][0]['id'])")

# Create a surrogate (you'll need to authenticate first)
curl -X POST http://localhost:8000/api/v1/manuscripts/surrogates/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "manuscript": "'$MANUSCRIPT_ID'",
    "folio_number": "1r",
    "surrogate_type": "scan",
    "image_url": "https://example.com/test-image.jpg",
    "width": 2000,
    "height": 3000,
    "file_format": "JPEG",
    "file_size": 1000000
  }'
```

### Option 3: Use Seed Script (if available)

```bash
cd backend
source venv/bin/activate
python manage.py seed_manuscripts --count 1
```

## Testing Checklist

- [ ] Can access manuscript list page
- [ ] Can click on a manuscript to view details
- [ ] "View Images" button appears when manuscript has surrogates
- [ ] Viewer page loads without errors
- [ ] Image displays in OpenSeadragon viewer
- [ ] Can zoom in/out
- [ ] Can pan around image
- [ ] Previous/Next buttons work
- [ ] Thumbnail navigation works
- [ ] Can switch between multiple images
- [ ] Header shows correct folio information
- [ ] Back button returns to manuscript details

## Next Steps After Testing

Once the viewer is working:
1. ✅ Test with multiple images
2. ✅ Test with high-resolution images
3. ✅ Test zoom/pan performance
4. ✅ Test on different screen sizes
5. ✅ Ready to add annotation features!


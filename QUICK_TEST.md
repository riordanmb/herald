# Quick Test Guide - Manuscript Viewer

## ✅ Setup Complete!

I've created a test surrogate for you. Here's how to test the viewer:

## Step 1: Start the Frontend (if not running)

```bash
cd frontend
npm run dev
```

Wait for: `✓ Ready in X.Xs` message

## Step 2: Open in Browser

**Option A: Start from Manuscript List**
1. Go to: **http://localhost:3000/manuscripts**
2. Click on **"MS Fr. 12595"** (or any manuscript)
3. Click the **"View Images"** button

**Option B: Direct Link**
Go directly to:
```
http://localhost:3000/manuscripts/{MANUSCRIPT_ID}/viewer
```

(Replace `{MANUSCRIPT_ID}` with the UUID shown below)

## Step 3: Test the Viewer

Once the viewer loads, you should see:

1. **Header Bar** with:
   - Back link to manuscript details
   - Manuscript shelfmark and folio number
   - "Image 1 of 1" counter
   - Previous/Next buttons

2. **Main Viewer Area** with:
   - OpenSeadragon image viewer
   - Navigation controls (zoom, pan, home, fullscreen)
   - The test image displayed

3. **Thumbnail Strip** (if multiple images):
   - Thumbnail images at the bottom
   - Click to jump to specific folio

## Step 4: Try These Actions

- ✅ **Zoom**: Scroll with mouse wheel or use +/- buttons
- ✅ **Pan**: Click and drag the image
- ✅ **Home**: Click home button to reset view
- ✅ **Fullscreen**: Click fullscreen button (if available)
- ✅ **Navigate**: Use Previous/Next buttons (when multiple images)

## Expected Results

✅ **Success**: Image loads, you can zoom/pan, controls work  
❌ **Issue**: See troubleshooting below

## Troubleshooting

### "No images available"
- Check that surrogates exist: Run the test surrogate creation script again
- Verify in admin: http://localhost:8000/admin

### Viewer blank/not loading
- Check browser console (F12) for errors
- Verify OpenSeadragon CDN is accessible
- Check network tab for failed image requests

### Image doesn't display
- The test uses a placeholder image service (picsum.photos)
- If it doesn't load, try uploading a real image via admin

## Next: Add More Test Images

To test navigation with multiple images:

1. Go to: http://localhost:8000/admin
2. Login: `admin` / `admin123`
3. Navigate to **Surrogates** → **Add Surrogate**
4. Create additional surrogates with different folio numbers (e.g., "2r", "3r")
5. Return to viewer and test navigation

## Ready for Annotations?

Once the viewer is working, we can add:
- Fabric.js canvas overlay
- Drawing tools (rectangles, polygons)
- Save/load annotations


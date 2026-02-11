# Next.js Dev Server Restart Required

## Issue
The Next.js dev server is stuck in an error state where it's looking for `_document.js` but won't compile `_document.tsx`. This is preventing the viewer page from loading.

## Solution
**Restart the Next.js dev server:**

1. Stop the current dev server (Ctrl+C in the terminal running `npm run dev`)
2. Clear the `.next` cache:
   ```bash
   cd /workspace/frontend
   rm -rf .next
   ```
3. Restart the dev server:
   ```bash
   npm run dev
   ```

## Why This Happens
After clearing the `.next` cache, Next.js needs to rebuild all pages. Sometimes the dev server gets stuck in an error state and needs a fresh restart to properly compile all files, including the Pages Router files (`_document.tsx`, `_app.tsx`) that are needed for error handling.

## Files Created
- `src/pages/_document.tsx` - Required for Next.js error handling
- `src/pages/_app.tsx` - Required for Next.js app wrapper
- `src/app/error.tsx` - App Router error boundary
- `src/app/not-found.tsx` - App Router 404 page

Once the dev server restarts, Next.js will compile these files and the viewer page should work correctly.


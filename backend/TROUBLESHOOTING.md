# Troubleshooting Guide

## Admin Page Shows Empty/Blank

If you're seeing an empty response when accessing `http://localhost:8000/admin`:

### Solution 1: Follow the Redirect
The admin page redirects to the login page if you're not authenticated. Try:
- `http://localhost:8000/admin/login/`
- Or let your browser follow the redirect automatically

### Solution 2: Collect Static Files
Django admin requires static files (CSS/JS) to display properly:

```bash
cd backend
source venv/bin/activate
python manage.py collectstatic --noinput
```

### Solution 3: Check Server is Running
Make sure the Django development server is running:

```bash
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### Solution 4: Clear Browser Cache
Sometimes browsers cache redirects. Try:
- Hard refresh: `Ctrl+Shift+R` (Linux/Windows) or `Cmd+Shift+R` (Mac)
- Or open in incognito/private mode

### Solution 5: Check Browser Console
Open browser developer tools (F12) and check:
- Network tab for failed requests
- Console for JavaScript errors
- Ensure static files are loading (CSS/JS)

## Common Issues

### "Empty Response" or Blank Page
- **Cause**: Browser not following redirect or static files not loading
- **Fix**: Access `/admin/login/` directly or collect static files

### "404 Not Found" for Static Files
- **Cause**: Static files not collected or URL configuration issue
- **Fix**: Run `python manage.py collectstatic`

### "Connection Refused"
- **Cause**: Django server not running
- **Fix**: Start server with `python manage.py runserver`

### "Permission Denied" in Admin
- **Cause**: Not logged in or not a superuser
- **Fix**: Create superuser with `python manage.py createsuperuser`

## Verifying Everything Works

1. **Check server is running:**
   ```bash
   curl http://localhost:8000/admin/
   ```
   Should return a 302 redirect to `/admin/login/`

2. **Check login page:**
   ```bash
   curl http://localhost:8000/admin/login/
   ```
   Should return HTML with login form

3. **Check static files:**
   ```bash
   curl http://localhost:8000/static/admin/css/base.css
   ```
   Should return CSS content

4. **Check API:**
   ```bash
   curl http://localhost:8000/api/v1/
   ```
   Should return API root JSON

## Getting Help

If issues persist:
1. Check Django logs: `tail -f backend/logs/django.log`
2. Check server output for errors
3. Verify database is accessible: `python manage.py check`
4. Ensure all migrations are applied: `python manage.py migrate`


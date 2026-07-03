# Render Deployment Checklist ✅

## Completed Setup Files

- ✅ `render.yaml` - Render configuration file
- ✅ `.renderignore` - Files to exclude from deployment
- ✅ `RENDER_DEPLOYMENT.md` - Detailed deployment guide
- ✅ `grocery/settings.py` - Updated with Render domain support

## Next Steps to Deploy

### 1. Prepare Your Repository
```bash
# From /home/john/Desktop/grocery_project/grocery_project/
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. Use Clean Production Requirements
Before deploying, ensure you're using production requirements:

```bash
# Option A: Copy production requirements to main requirements.txt
cp requirements-prod.txt requirements.txt
git add requirements.txt
git commit -m "Use production dependencies"
git push origin main
```

**Current requirements-prod.txt:**
- Django==4.2.30
- gunicorn==21.2.0
- psycopg2-binary==2.9.9
- dj-database-url==2.1.0
- whitenoise==6.5.0
- python-decouple==3.8

### 3. Deploy on Render
1. Go to https://dashboard.render.com
2. Click "New" → "PostgreSQL"
   - Create database `grocery_prod`
   - Copy the Internal Database URL
3. Click "New" → "Web Service"
   - Connect your GitHub repository
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn grocery.wsgi:application --bind 0.0.0.0:$PORT`
4. Add Environment Variables:
   - `DJANGO_DEBUG` = `False`
   - `DJANGO_SECRET_KEY` = [Generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"]
   - `DATABASE_URL` = [Internal DB URL from step 2]
   - `DJANGO_ALLOWED_HOSTS` = `yourdomain.onrender.com`
   - `PYTHON_VERSION` = `3.11`

### 4. Run Initial Migrations
After first deployment:
1. Click "Shell" in your Render web service
2. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

### 5. Test & Monitor
- Visit your app URL (e.g., https://grocery-app.onrender.com)
- Check logs in Render dashboard for errors
- Test login and key features

## Environment Variables Summary

| Variable | Required | Example |
|----------|----------|---------|
| `DJANGO_DEBUG` | Yes | `False` |
| `DJANGO_SECRET_KEY` | Yes | `[long random string]` |
| `DATABASE_URL` | Yes | `postgresql://user:pass@host:port/db` |
| `DJANGO_ALLOWED_HOSTS` | Yes | `yourdomain.onrender.com` |
| `DJANGO_SETTINGS_MODULE` | No | `grocery.settings` |
| `PYTHON_VERSION` | No | `3.11` |

## Important Notes

⚠️ **Production Deployment**:
- Use Starter plan ($7/month) for reliability
- Don't use free tier for production (services spin down after 15 min inactivity)
- Always use HTTPS (enabled by default on Render)
- Ensure DATABASE_URL and SECRET_KEY are set correctly

📝 **For Custom Domain**:
- After deploying on Render, update DNS records pointing to Render
- Add domain to `DJANGO_ALLOWED_HOSTS` in Render environment

🔄 **Continuous Deployment**:
- Push to GitHub → Render automatically deploys
- Check dashboard for deployment status and logs

---

**Read RENDER_DEPLOYMENT.md for full detailed guide with troubleshooting.**

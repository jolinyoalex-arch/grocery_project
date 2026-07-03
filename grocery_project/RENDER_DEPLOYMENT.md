# Render Deployment Guide for Grocery Project

## Prerequisites

1. **Render Account**: Sign up at https://render.com (free tier available)
2. **GitHub Account**: Push your code to GitHub (Render deploys from GitHub)

## Step 1: Prepare Your Repository

Make sure your code is pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Step 2: Set Up PostgreSQL Database on Render

1. Log in to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "PostgreSQL"
3. Fill in the details:
   - **Name**: `grocery-db` (or any name)
   - **Database**: `grocery_prod`
   - **User**: `postgres` (default)
   - **Region**: Choose your preferred region
   - **Plan**: Free (for testing) or Starter ($7/month for production)
4. Click "Create Database"
5. Wait for the database to be created (takes ~1-2 minutes)
6. Copy the **Internal Database URL** - you'll need this for your web service

## Step 3: Create Web Service on Render

1. Click "New" → "Web Service"
2. Connect to your GitHub repository:
   - Search for your `grocery_project` repository
   - Click "Connect"
3. Fill in the configuration:
   - **Name**: `grocery-app` (or any name)
   - **Environment**: `Python 3`
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**:
     ```
     gunicorn grocery.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - **Plan**: Free (for testing) or Starter ($7/month for production)

## Step 4: Add Environment Variables

In the "Environment" section, add these variables:

| Key | Value |
|-----|-------|
| `DJANGO_DEBUG` | `False` |
| `DJANGO_SETTINGS_MODULE` | `grocery.settings` |
| `DJANGO_SECRET_KEY` | [Generate below] |
| `DJANGO_ALLOWED_HOSTS` | `yourdomain.onrender.com,yourdomain.com` |
| `DATABASE_URL` | [Internal DB URL from Step 2] |
| `PYTHON_VERSION` | `3.11` |

### Generate Django Secret Key

Run this command locally:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as `DJANGO_SECRET_KEY`.

## Step 5: Update requirements.txt

Your production requirements should include:

```
Django==4.2.30
gunicorn==21.2.0
psycopg2-binary==2.9.9
dj-database-url==2.1.0
whitenoise==6.5.0
python-decouple==3.8
```

**Option A**: Update your main requirements.txt:
```bash
cp requirements.txt requirements.txt.bak
cp requirements-prod.txt requirements.txt
git add requirements.txt
git commit -m "Use production requirements"
git push origin main
```

**Option B**: Use requirements-prod.txt in Render's Build Command:
```
pip install -r requirements-prod.txt && python manage.py collectstatic --noinput
```

## Step 6: Deploy

1. Click "Create Web Service"
2. Render will start building your app (watch the logs)
3. Once deployment is successful, you'll see a URL like `https://grocery-app.onrender.com`

## Step 7: Run Initial Migrations

The first deployment will fail if the database isn't migrated. You can:

### Option A: Run migrations manually (Recommended for first time)
1. After deployment, go to the web service settings
2. Click "Shell" at the top
3. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Option B: Auto-migrate on deploy
Add this to the Build Command:
```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

## Step 8: Configure Custom Domain (Optional)

1. In your web service settings, go to "Settings"
2. Under "Custom Domains", add your domain
3. Follow the DNS configuration steps

## Step 9: Set Up Static Files & Media

Render automatically serves static files with WhiteNoise. Make sure:

1. `STATIC_URL = '/static/'` in settings.py ✅
2. `STATIC_ROOT = BASE_DIR / 'staticfiles'` in settings.py ✅
3. WhiteNoise is installed ✅
4. Run: `python manage.py collectstatic --noinput`

## Troubleshooting

### Deploy fails with ModuleNotFoundError
- Check that all required packages are in `requirements.txt`
- Ensure `requirements.txt` uses the production versions

### Static files not loading (CSS/JS missing)
- Run: `python manage.py collectstatic --noinput`
- Check that `STATIC_ROOT` is set correctly
- Verify WhiteNoise middleware is installed

### Database connection errors
- Verify `DATABASE_URL` environment variable is correct
- Check the internal database URL from Render
- Ensure the database is in the same region

### 502 Bad Gateway error
- Check the app logs in Render dashboard
- Look for Python errors in the output
- Verify the Start Command is correct

## Monitoring & Logs

1. Go to your web service in Render dashboard
2. Click "Logs" tab to see real-time logs
3. Look for Django errors, stack traces, and deployment messages

## Auto-Deploy on GitHub Push

Render automatically redeploys when you push to the connected branch:

```bash
# Make changes locally
git add .
git commit -m "Update grocery app"
git push origin main

# Render will automatically start a new deploy!
```

## Free Tier Limitations

- Web service spins down after 15 minutes of inactivity
- Database backups are limited
- No custom domains on free tier

**Recommended for production**: Upgrade to at least Starter ($7/month web + $5/month database)

---

**Need help?** Check [Render Documentation](https://render.com/docs) or [Django Deployment Guide](https://docs.djangoproject.com/en/4.2/howto/deployment/)

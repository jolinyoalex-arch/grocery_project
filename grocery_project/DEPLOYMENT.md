# Vercel Deployment Guide for Grocery Project

## Prerequisites

1. **Vercel Account**: Sign up at https://vercel.com
2. **PostgreSQL Database**: Set up a PostgreSQL database (you can use:
   - [Neon](https://neon.tech) - Free PostgreSQL hosting
   - [Railway](https://railway.app) - Paid but developer-friendly
   - [AWS RDS](https://aws.amazon.com/rds/) - Enterprise option
   - [Render](https://render.com) - Easy PostgreSQL hosting

## Step 1: Update Requirements

Replace your current `requirements.txt` with the production version:

```bash
cp requirements-prod.txt requirements.txt
```

Or install the production packages:

```bash
pip install -r requirements-prod.txt
```

## Step 2: Set Up PostgreSQL Database

Choose one of these options:

### Option A: Using Neon (Recommended - Free)
1. Go to https://neon.tech and sign up
2. Create a new project
3. Copy your database connection string (starts with `postgresql://`)
4. Save it somewhere safe

### Option B: Using Railway
1. Go to https://railway.app and sign up
2. Create a new PostgreSQL database
3. Copy the connection string

## Step 3: Generate Django Secret Key

Generate a secure secret key for production:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output - you'll need it for Vercel.

## Step 4: Create Vercel Project

1. **Install Vercel CLI** (optional but helpful):
   ```bash
   npm i -g vercel
   ```

2. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

3. **Create Vercel Project**:
   - Go to https://vercel.com/dashboard
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Select the repository

## Step 5: Configure Environment Variables

In your Vercel project settings, add these environment variables:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Your PostgreSQL connection string |
| `DJANGO_SECRET_KEY` | The secret key you generated in Step 3 |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `yourdomain.vercel.app` or your custom domain |

### Example DATABASE_URL:
```
postgresql://user:password@host:5432/database
```

## Step 6: Run Database Migrations

After deploying, run migrations on Vercel:

```bash
vercel env pull  # Pull environment variables locally
python manage.py migrate
```

Or you can create a `migrate.py` script and run it on first deploy.

## Step 7: Create Superuser (Optional)

If you want to access the Django admin:

```bash
vercel shell
python manage.py createsuperuser
```

## Step 8: Collect Static Files

Static files are automatically collected during deployment via the `vercel.json` configuration.

## Step 9: Deploy

Option 1: **Using Vercel CLI**
```bash
vercel --prod
```

Option 2: **Using GitHub (Auto-deployment)**
- Push to your main branch
- Vercel automatically deploys when you push

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution**: Update `requirements.txt` to use `requirements-prod.txt`

### Issue: "Database connection refused"
**Solution**: 
1. Check your `DATABASE_URL` is correct in Vercel environment variables
2. Ensure your database allows connections from Vercel's IP ranges
3. Check database user permissions

### Issue: "Static files not loading"
**Solution**:
1. Run `python manage.py collectstatic`
2. Check that WhiteNoise middleware is properly configured in `settings.py`

### Issue: "Secret key is insecure"
**Solution**:
1. Generate a new secret key (see Step 3)
2. Update `DJANGO_SECRET_KEY` in Vercel environment variables

### Issue: "CSRF token missing or incorrect"
**Solution**:
1. Ensure your domain is in `CSRF_TRUSTED_ORIGINS` in `settings.py`
2. Set `ALLOWED_DOMAIN` environment variable if using custom domain

## Setting Up Custom Domain

1. In Vercel dashboard, go to Settings → Domains
2. Add your custom domain
3. Update your domain's DNS records to point to Vercel
4. Add your domain to `ALLOWED_DOMAIN` environment variable

## Monitoring

Monitor your deployment at:
- https://vercel.com/dashboard → Your Project
- Check logs for any errors
- Use `vercel logs` command locally

## Useful Commands

```bash
# Pull environment variables
vercel env pull

# View logs
vercel logs

# Deploy
vercel --prod

# List deployments
vercel list
```

## Security Checklist

- [ ] Set a strong `DJANGO_SECRET_KEY`
- [ ] Set `DEBUG = False` in production
- [ ] Use HTTPS only
- [ ] Secure your database with strong credentials
- [ ] Restrict database access to Vercel IP range
- [ ] Keep dependencies updated
- [ ] Set up proper error logging

## Additional Resources

- [Django Deployment Guide](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Vercel Python Guide](https://vercel.com/docs/runtimes/python)
- [WhiteNoise Documentation](https://whitenoise.evans.io/)
- [dj-database-url](https://github.com/jazzband/dj-database-url)

## Next Steps

1. Choose a PostgreSQL provider from Step 2
2. Generate a secret key (Step 3)
3. Push code to GitHub
4. Create Vercel project and add environment variables
5. Deploy and test your application

Good luck with your deployment! 🚀

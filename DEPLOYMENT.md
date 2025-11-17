# Railway Deployment Guide

## Credentials Management System - Educational Demo

This project is configured for deployment on Railway.

### Pre-Deployment Checklist

✅ Microsoft branding removed
✅ Educational disclaimers added
✅ Production-ready settings configured
✅ Whitenoise for static files
✅ Gunicorn as WSGI server

### Railway Deployment Steps

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect this repository

3. **Add PostgreSQL Database** (Optional, currently uses SQLite)
   - In your project, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will auto-configure DATABASE_URL

4. **Set Environment Variables**
   Click on your service → Variables → Add these:
   ```
   SECRET_KEY=your-secret-key-here-generate-a-random-one
   DEBUG=False
   ALLOWED_HOSTS=yourapp.railway.app
   ```

5. **Generate SECRET_KEY**
   Run locally:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. **Deploy**
   - Railway will automatically detect Django
   - It will run migrations
   - App will be available at: `https://yourapp.railway.app`

7. **Create Superuser** (After deployment)
   - Go to Railway dashboard → your service
   - Click "Shell" tab
   - Run: `python manage.py createsuperuser`

8. **Generate Credential Links**
   In Railway shell:
   ```bash
   python manage.py generate_credential_links
   ```

### Important Notes

- ⚠️ **Educational Purpose**: This tool includes clear disclaimers
- 🔒 **Security**: Change SECRET_KEY in production
- 📊 **Database**: SQLite for demo, use PostgreSQL for production
- 🌐 **Domain**: Update ALLOWED_HOSTS with your domain

### Admin Access

After deployment, access admin at:
`https://yourapp.railway.app/admin/`

### View Submissions

All credential submissions appear at:
`https://yourapp.railway.app/admin/credentials/credentialsubmission/`

### Monitoring

Railway provides:
- Real-time logs
- CPU/Memory usage
- Automatic HTTPS
- Custom domain support

### Cost

- $5/month free credit
- ~$0.000231/min for compute
- ~$0.25/GB for PostgreSQL

### Support

For issues, check Railway documentation:
https://docs.railway.app/

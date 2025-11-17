# Credentials Management System

**Educational Security Awareness Tool**

⚠️ **DISCLAIMER**: This is an educational demonstration tool for security awareness training. It includes visible disclaimers and is not designed for malicious use.

## Features

- Token-based credential collection links
- Educational security awareness interface  
- Admin panel for viewing submissions
- IP address logging
- Link expiration system
- Educational disclaimers on all pages

## Local Development

### Requirements
- Python 3.12+
- Django 4.2.7

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create superuser:
```bash
python manage.py createsuperuser
```

4. Run server:
```bash
python manage.py runserver
```

5. Generate credential link:
```bash
python manage.py generate_credential_links
```

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for Railway deployment instructions.

### Environment Variables

```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

## Usage

1. Generate a secure link using the management command
2. Link expires after 30 days (configurable)
3. Users enter credentials through the link
4. View submissions in admin panel at `/admin/`

## Admin Access

- URL: `/admin/`
- View submissions: `/admin/credentials/credentialsubmission/`

## Project Structure

```
Project/
├── config/              # Django settings
├── credentials/         # Main app
│   ├── templates/      # HTML templates
│   ├── management/     # Custom commands
│   └── models.py       # Database models
├── requirements.txt    # Python dependencies
├── Procfile           # Railway/Heroku config
└── runtime.txt        # Python version
```

## Security Features

- CSRF protection
- Password hashing (PBKDF2)
- Session security
- IP logging
- Educational disclaimers

## Educational Purpose

This tool is designed for:
- Security awareness training
- Demonstrating phishing techniques
- Teaching credential security
- IT security education

## License

Educational use only. Not for unauthorized credential collection.

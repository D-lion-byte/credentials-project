# Secure Credentials Management System

A Django-based secure credential management system that allows users to update their email, username, and password through a protected web interface.

## 🔐 Security Features

- **Password Hashing**: Uses Django's PBKDF2 algorithm for secure password storage
- **CSRF Protection**: All forms include CSRF tokens
- **Authentication Required**: Users must be logged in to access credential update page
- **Password Validation**: Enforces strong password requirements
- **Session Security**: Automatic session management and timeouts
- **Input Validation**: Comprehensive validation for all user inputs
- **Unique Constraints**: Prevents duplicate usernames and emails

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## 🚀 Setup Instructions

### 1. Install PostgreSQL

Download and install PostgreSQL from: https://www.postgresql.org/download/

### 2. Create Database

Open PostgreSQL command line (psql) and run:

```sql
CREATE DATABASE credentials_db;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE credentials_db TO postgres;
```

### 3. Update Database Settings

Edit `storefront/settings.py` and update the PostgreSQL password:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'credentials_db',
        'USER': 'postgres',
        'PASSWORD': 'your_actual_password',  # Change this!
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4. Install Python Dependencies

```powershell
pip install django psycopg2-binary
```

### 5. Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Run the Development Server

```powershell
python manage.py runserver
```

## 🌐 Usage

### Access Points

1. **Information Page**: `http://127.0.0.1:8000/credentials/`
   - Landing page with security information
   - Explains the credential update process

2. **Update Credentials**: `http://127.0.0.1:8000/credentials/update/`
   - Secure form to update email, username, and password
   - Requires authentication

3. **Admin Panel**: `http://127.0.0.1:8000/admin/`
   - Django admin interface
   - Login with superuser credentials

### How to Update Credentials

1. Navigate to `http://127.0.0.1:8000/admin/` and log in
2. After logging in, go to `http://127.0.0.1:8000/credentials/update/`
3. Fill in the form:
   - **Email**: Enter your new email address
   - **Username**: Enter your new username
   - **Current Password**: Enter your current password (required for verification)
   - **New Password**: Enter a new password (optional - leave blank to keep current)
   - **Confirm Password**: Re-enter the new password
4. Click "Update Credentials"
5. You'll see a success message if the update was successful

## 🛡️ Security Best Practices

### For Development

1. **Never commit sensitive data**: Keep your `SECRET_KEY` and database passwords secure
2. **Use HTTPS**: In production, always use HTTPS
3. **Environment Variables**: Store sensitive settings in environment variables
4. **Update Dependencies**: Keep Django and all packages up to date

### For Production

Update `settings.py` before deploying:

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')  # Use environment variable

# Enable HTTPS security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

## 📁 Project Structure

```
Project/
├── credentials/               # Credential management app
│   ├── templates/
│   │   └── credentials/
│   │       ├── update_credentials.html
│   │       └── info.html
│   ├── forms.py              # Secure form with validation
│   ├── views.py              # Protected views
│   ├── urls.py               # URL routing
│   └── models.py             # Uses Django's User model
├── storefront/               # Main project settings
│   ├── settings.py           # PostgreSQL configuration
│   └── urls.py               # Main URL routing
└── manage.py
```

## 🔧 Validation Rules

### Username
- 150 characters or fewer
- Letters, digits, and @/./+/-/_ only
- Must be unique

### Email
- Valid email format
- Must be unique

### Password
- Minimum 8 characters
- Cannot be too similar to username or email
- Cannot be entirely numeric
- Cannot be a commonly used password

## 📝 API Endpoints

| URL | Method | Description | Auth Required |
|-----|--------|-------------|---------------|
| `/credentials/` | GET | Information page | No |
| `/credentials/update/` | GET/POST | Update credentials form | Yes |
| `/admin/` | GET/POST | Django admin | Yes |

## 🐛 Troubleshooting

### Database Connection Error

If you see `psycopg2.OperationalError`:
- Check PostgreSQL is running
- Verify database name, username, and password
- Ensure PostgreSQL is listening on port 5432

### Import Error for psycopg2

Run:
```powershell
pip install psycopg2-binary
```

### CSRF Token Error

- Ensure Django's CSRF middleware is enabled
- Make sure `{% csrf_token %}` is in all forms
- Clear browser cookies and try again

## 📚 Learn More

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Security Best Practices](https://docs.djangoproject.com/en/stable/topics/security/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## ⚠️ Important Notes

- This system is designed for **legitimate business use only**
- Never use this for phishing or unauthorized access
- Always inform users about credential updates through official channels
- Implement additional authentication (2FA) for production use
- Regular security audits are recommended

## 📄 License

This project is for educational and legitimate business purposes only.

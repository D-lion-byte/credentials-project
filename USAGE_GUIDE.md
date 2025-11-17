# 🔐 Secure Private Link Credential Update System

## Overview
A Microsoft-style secure credential update system that allows office staff to send private links to users via email. Users can update their email, username, and password without needing to know their current password.

## ✨ Key Features

- **Private Secure Links**: Each user gets a unique, cryptographically secure link
- **No Login Required**: Token in the URL authenticates the user automatically
- **Time-Limited**: Links expire after 24-48 hours (configurable)
- **Single-Use**: Each link can only be used once for security
- **Microsoft-Style UI**: Clean, professional interface like Microsoft account updates
- **Email-Friendly**: Perfect for sending to users from office emails

## 🚀 How to Use

### For Office Staff (Sending Links)

#### 1. Generate a Private Link for a Single User

By username:
```powershell
python manage.py generate_credential_links --username john_doe
```

By email:
```powershell
python manage.py generate_credential_links --email john@company.com
```

With custom expiration (in hours):
```powershell
python manage.py generate_credential_links --username john_doe --hours 48
```

#### 2. Generate Links for All Users

```powershell
python manage.py generate_credential_links --all
```

#### 3. Copy the Link and Send via Email

Example email template:
```
Subject: Update Your Account Credentials

Dear User,

Please update your account credentials by clicking the secure link below:

http://127.0.0.1:8000/credentials/update/[TOKEN_HERE]/

This link will expire in 24 hours for your security.

If you did not request this update, please contact IT support immediately.

Best regards,
IT Department
```

### For Users (Updating Credentials)

1. **Click the link** sent by office staff
2. **Fill in the form**:
   - New email address
   - New username
   - New password (twice for confirmation)
3. **Click "Update"**
4. **See success message** - Microsoft-style confirmation

**No current password needed!** The secure link authenticates them.

## 🔗 Available URLs

| URL | Purpose |
|-----|---------|
| `/credentials/` | Information page about the system |
| `/credentials/update/[TOKEN]/` | Private link for credential update |
| `/credentials/success/` | Success confirmation page |
| `/admin/` | Django admin panel |

## 🛠️ Management Commands

### Generate Private Links

```powershell
# Single user by username
python manage.py generate_credential_links --username admin

# Single user by email  
python manage.py generate_credential_links --email admin@test.com

# All users at once
python manage.py generate_credential_links --all

# Custom expiration time
python manage.py generate_credential_links --username admin --hours 48
```

### View Tokens in Admin

1. Go to `http://127.0.0.1:8000/admin/`
2. Login with your admin credentials
3. Click "Credential Update Tokens"
4. See all active, expired, and used tokens

## 🔐 Security Features

✅ **Cryptographically Secure Tokens**: Uses Python's `secrets` module  
✅ **Time-Limited Access**: Links expire automatically  
✅ **Single-Use Tokens**: Can't be reused after update  
✅ **Password Hashing**: All passwords use PBKDF2 encryption  
✅ **CSRF Protection**: All forms include CSRF tokens  
✅ **Input Validation**: Prevents weak passwords and duplicate accounts  
✅ **No Current Password**: Users don't need to remember old password  

## 📧 Email Integration Tips

### For Gmail/Outlook (Development)
```python
# Add to settings.py for email testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### For Production Email
```python
# Add to settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@company.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 🎨 UI Design

The interface uses Microsoft's design language:
- **Segoe UI font** - Official Microsoft font
- **Microsoft color scheme** - #0078d4 (blue), #107c10 (green)
- **Clean, minimal design** - Professional look
- **Responsive** - Works on mobile and desktop

## ⚙️ Configuration

### Change Link Expiration Time

Default is 24 hours. To change:
```python
# In models.py, modify the generate_token method
token = CredentialUpdateToken.generate_token(user, hours_valid=48)
```

Or use the command line flag:
```powershell
python manage.py generate_credential_links --username admin --hours 72
```

### Database

Currently using SQLite for development. For production, uncomment PostgreSQL settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'credentials_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🔄 Workflow Example

1. **Office receives request** - User calls/emails saying they forgot password
2. **Generate link** - `python manage.py generate_credential_links --username user123`
3. **Copy the link** - From terminal output
4. **Send via email** - Paste link in email to user
5. **User clicks link** - Opens form in browser
6. **User updates info** - Enters new email, username, password
7. **Success!** - User sees Microsoft-style success page
8. **Link expires** - Can't be used again

## 📊 Monitoring

### Check Token Status
```powershell
python manage.py shell
```

Then:
```python
from credentials.models import CredentialUpdateToken

# See all tokens
CredentialUpdateToken.objects.all()

# See active tokens
CredentialUpdateToken.objects.filter(is_used=False)

# See expired tokens
from django.utils import timezone
CredentialUpdateToken.objects.filter(expires_at__lt=timezone.now())
```

## 🚨 Troubleshooting

### "Link expired or already used"
- Token was already used once
- Token expired (24+ hours old)
- Generate a new link for the user

### "Current password is incorrect"
- This shouldn't happen with token links!
- Make sure user is using the `/credentials/update/[TOKEN]/` URL
- Check that `via_token=True` is set in the view

### Server not starting
- Check if port 8000 is in use
- Try: `python manage.py runserver 8080`

## 📝 Example Link
```
http://127.0.0.1:8000/credentials/update/DBIw10-CnnE-A1bq_uYzak0JqzV6eRbvx7xcgLdk9K5fOaZoGaFrH8Mijfkr4fA9/
```

This link:
- ✅ Authenticates the user automatically
- ✅ Shows clean Microsoft-style form
- ✅ Allows password update without current password
- ✅ Expires in 24 hours
- ✅ Works only once

## 🎯 Perfect For

- Password reset requests from users
- New employee onboarding
- Bulk credential updates
- Security-mandated password changes
- Account recovery processes

---

**Remember**: Always send these links through secure channels (official company email) and never share them publicly!

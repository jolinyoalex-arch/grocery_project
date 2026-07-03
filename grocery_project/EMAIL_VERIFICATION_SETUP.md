# Email Verification Setup Guide

This guide explains how to set up email verification codes for user registration.

## Overview

When users register, they will:
1. Fill in registration form
2. Receive a 6-digit verification code via email
3. Enter the code on the verification page
4. Get access to the app after successful verification

## Setup Steps

### Step 1: Database Migration

Create and run migrations for the new `VerificationCode` model:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Development Setup (Console Email)

For development, emails will print to the console instead of sending. No configuration needed!

```bash
# In your .env or environment
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

When users register, the verification code will appear in your terminal:

```
Subject: Email Verification Code
From: noreply@grocery.com
To: user@example.com

Hello username,

Thank you for registering with us!

Your email verification code is:

    123456

This code will expire in 10 minutes.
```

### Step 3: Production Setup (Send Real Emails)

Choose one of these options:

#### Option A: Gmail with App Password (Recommended for testing)

1. **Enable 2-Factor Authentication on your Google Account**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Google will generate a 16-character password
   - Copy this password

3. **Update your environment variables:**

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx  # The 16-char password from step 2
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

#### Option B: SendGrid (Recommended for production)

1. **Create a free SendGrid account**
   - Go to https://sendgrid.com
   - Sign up for a free account

2. **Create API Key**
   - Go to Settings → API Keys
   - Click "Create API Key"
   - Copy the key

3. **Update your environment variables:**

```bash
EMAIL_BACKEND=sendgrid_backend.SendgridBackend
SENDGRID_API_KEY=SG.your-api-key-here
```

4. **Install sendgrid package:**

```bash
pip install sendgrid-django
pip freeze > requirements.txt
```

#### Option C: Mailgun (Alternative)

1. **Create Mailgun account**
   - Go to https://www.mailgun.com
   - Sign up for free tier

2. **Update environment variables:**

```bash
EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend
ANYMAIL={"MAILGUN_API_KEY": "key-your-key-here"}
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

3. **Install package:**

```bash
pip install django-anymail[mailgun]
pip freeze > requirements.txt
```

### Step 4: Update Django Settings

The settings are already configured in `grocery/settings.py`. They read from environment variables:

```python
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@grocery.com')
```

### Step 5: Test Email Sending

```bash
python manage.py shell

# Test SendMail
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Subject',
    'Test message body',
    settings.DEFAULT_FROM_EMAIL,
    ['your-test-email@example.com'],
    fail_silently=False,
)
```

## How It Works

### Registration Flow

1. User fills registration form → POST to `/register/`
2. Backend creates User (is_active=True)
3. Backend generates 6-digit verification code
4. Backend sends email with code
5. User redirected to `/verify-email/`
6. User enters code → POST to `/verify-email/`
7. Backend validates code (must be valid and not expired)
8. If valid: mark email as verified, log user in, redirect to home
9. If invalid: show error, ask to try again

### Verification Code Details

- **Format**: 6 random digits
- **Expiration**: 10 minutes
- **Validation**: Not used, not expired, correct code
- **Resend**: User can click "Resend Code" button
- **Storage**: Database (VerificationCode model)

### Key URLs

- `/register/` - Registration form
- `/verify-email/` - Verification code entry
- `/resend-verification-code/` - Resend code

## Troubleshooting

### "Failed to send verification email"

**Problem**: Email backend not configured

**Solutions**:
1. Check EMAIL_BACKEND in environment variables
2. Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
3. For Gmail, ensure you used App Password, not regular password
4. Check firewall/network settings

### "SMTPAuthenticationError"

**Problem**: Wrong email credentials

**Solution**:
1. Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
2. For Gmail, regenerate App Password
3. Check that EMAIL_PORT is correct (587 for TLS, 465 for SSL)

### Email not received

**Problem**: 
1. Check spam/junk folder
2. Verify FROM email address is correct
3. Check email logs in your email service

**Solution**:
```bash
python manage.py shell
from django.core.mail import outbox
# Check if emails were sent to console backend
for email in outbox:
    print(f"To: {email.to}, Subject: {email.subject}")
```

## Customizing Email Template

Edit the email content in `orderingapp/views.py` in the `register_view` function:

```python
message = f'''
Hello {username},

Your email verification code is:

    {verification_code.code}

This code will expire in 10 minutes.

Best regards,
Grocery Store Team
'''
```

## Admin Interface

You can view verification codes in Django admin:

1. Go to `/admin/`
2. Click "Verification codes"
3. See all pending and used codes
4. Delete expired codes if needed

## Security Notes

- Codes are randomly generated 6-digit numbers
- Codes expire after 10 minutes
- Old codes are automatically deleted when new ones are requested
- Once used, codes cannot be reused
- User password is secure even without email verification

## For Vercel Deployment

When deploying to Vercel, set these environment variables:

1. `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` (if using SMTP)
2. `EMAIL_HOST=smtp.gmail.com` (or your provider)
3. `EMAIL_PORT=587`
4. `EMAIL_USE_TLS=True`
5. `EMAIL_HOST_USER=your-email@gmail.com`
6. `EMAIL_HOST_PASSWORD=your-password-or-api-key`
7. `DEFAULT_FROM_EMAIL=noreply@yourdomain.com`

## Next Steps

1. Run migrations: `python manage.py makemigrations && python manage.py migrate`
2. Update `.env` file with email settings
3. Test registration flow locally
4. Configure email service for production (Vercel)
5. Deploy and test!

For questions or issues, check the logs or Django console output.

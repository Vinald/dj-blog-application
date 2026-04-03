# Django Blog Application

A modern, feature-rich Django blog application with user authentication, post management, and password reset functionality.

## Features

- User registration and login
- User profile management with profile pictures
- Create, read, update, and delete blog posts
- View all posts from specific authors
- Password reset via email
- Pagination for blog posts
- Responsive Bootstrap UI
- Custom error pages (403, 404, 500)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate environment: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy environment file: `cp .env.example .env`
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Run server: `python manage.py runserver`

Access application at: http://localhost:8000

## Environment Configuration

### For Development Use: `.env.example`

During development:

1. Copy the template:
   ```
   cp .env.example .env
   ```

2. The default settings are configured for local development:
   - EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   - Emails print to your terminal/console
   - No real email provider needed

3. When you request a password reset:
   - Check your terminal/console for the reset link
   - Copy the link and paste in browser to test

### Environment Variables in Settings

The application now loads all email configuration from `.env` file:

```python
# In settings.py:
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 25))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@blog.example.com')
PASSWORD_RESET_TIMEOUT = int(os.getenv('PASSWORD_RESET_TIMEOUT', 3600))
```

Available Variables in `.env`:
- `EMAIL_BACKEND` - Email backend service (console or smtp)
- `EMAIL_HOST` - SMTP server address
- `EMAIL_PORT` - SMTP port
- `EMAIL_USE_TLS` - Enable TLS (True/False)
- `EMAIL_HOST_USER` - SMTP username or email
- `EMAIL_HOST_PASSWORD` - SMTP password or app password
- `DEFAULT_FROM_EMAIL` - Default sender email address
- `PASSWORD_RESET_TIMEOUT` - Reset link expiration in seconds

### For Production Use: `.env.production.example`

When deploying to production:

1. Copy production template:
   ```
   cp .env.production.example .env.production
   ```

2. Configure your email provider (choose one):

   **Gmail:**
   - Enable 2FA on Google account
   - Generate App Password: https://myaccount.google.com/apppasswords
   - Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD

   **SendGrid:**
   - Create account: https://sendgrid.com
   - Use provided SMTP credentials

   **AWS SES:**
   - Set up in AWS Console
   - Generate SMTP credentials
   - Update .env.production

   **Mailgun:**
   - Create account: https://www.mailgun.com
   - Get SMTP details from domain settings

3. Set DEBUG=False
4. Set ALLOWED_HOSTS with your domain
5. Generate new SECRET_KEY

### Important Notes

- Development: `.env` file is used locally
- Production: `.env.production` file only on server
- Never commit `.env` or `.env.production` files
- Keep example files (`.env.example`, etc.) in git for documentation

## Usage

### Authentication

- Register: `/account/register/`
- Login: `/account/login/`
- Password Reset: Click "Forgot password?" on login
- Profile: `/account/profile/`
- Logout: Click logout in navbar

### Blog Posts

- View all posts: `/` or `/posts/`
- View author posts: Click author name
- Create post: Click "New Post" (login required)
- Edit post: Click "Edit" on your posts
- Delete post: Click "Delete" on your posts

### Admin

Access admin panel: http://localhost:8000/admin/

## Testing

Create sample data:
```
python manage.py populate_posts
```

This creates demo user (username: demo, password: demo123) and 50 posts.

## Project Structure

```
Django-Blog-Application/
├── account/              # Authentication and profiles
├── post/                 # Blog posts
├── core/                 # Settings
├── templates/            # HTML templates
├── static/              # CSS files
├── media/               # User uploads
├── .env.example         # Development template
├── .env.local.example   # Local template
└── .env.production.example  # Production template
```

## Troubleshooting

**Emails not showing:**
- Check .env has EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
- Check terminal where you ran `python manage.py runserver`

**Database errors:**
- Run: `python manage.py migrate`
- Reset: `rm db.sqlite3` then `python manage.py migrate`

**Port already in use:**
- Use different port: `python manage.py runserver 8001`

**Static files missing:**
- Run: `python manage.py collectstatic`

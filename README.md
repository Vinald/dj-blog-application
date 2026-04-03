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
- Comprehensive test coverage
- Docker and Docker Compose support
- PostgreSQL database support
- Environment-based configuration

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Docker (optional, for containerized setup)

### Quick Start (Local Development)

1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Setup environment: `cp .env.example .env`
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Run server: `python manage.py runserver`

Access application at: http://localhost:8000

### Quick Start (Docker)

1. Ensure Docker and Docker Compose are installed
2. Make script executable: `chmod +x docker.sh`
3. Start application: `./docker.sh up`
4. Create superuser when prompted
5. Access application at: http://localhost:8000
6. Stop application: `./docker.sh down`

## Environment Configuration

The application uses a single `.env` file for configuration.

### Setup

```bash
cp .env.example .env
```

Edit `.env` with your values:

**Development:**
```
SECRET_KEY=your-secret-key
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@yourblog.com
PASSWORD_RESET_TIMEOUT=3600
```

**Production:**
```
SECRET_KEY=generate-new-key
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourblog.com
PASSWORD_RESET_TIMEOUT=3600
```

### Variables

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Django secret key (generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`) |
| `EMAIL_BACKEND` | `django.core.mail.backends.console.EmailBackend` (dev) or `django.core.mail.backends.smtp.EmailBackend` (production) |
| `EMAIL_HOST` | SMTP server (e.g., smtp.gmail.com) |
| `EMAIL_PORT` | SMTP port (usually 587) |
| `EMAIL_USE_TLS` | True or False |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password or app password |
| `DEFAULT_FROM_EMAIL` | Sender email address |
| `PASSWORD_RESET_TIMEOUT` | Reset link validity in seconds (3600 = 1 hour) |

### Email Providers

**Gmail:** Generate App Password at https://myaccount.google.com/apppasswords

**SendGrid, AWS SES, Mailgun:** Use their SMTP credentials

### Security

- **Never commit `.env` file** - Only `.env.example` should be in git
- **Development:** Emails print to console - no provider needed
- **Production:** Use real SMTP provider and enable security settings


## Usage

### Authentication

- Register: `/account/register/`
- Login: `/account/login/`
- Forgot Password: Click "Forgot password?" on login
- Profile: `/account/profile/`
- Logout: Navbar logout button

### Blog Posts

- View all: `/` or `/posts/`
- View by author: Click author name
- Create: Click "New Post" (login required)
- Edit: Click "Edit" on your posts
- Delete: Click "Delete" on your posts

### Admin Panel

Access at: http://localhost:8000/admin/

## Testing

Create sample data:
```bash
python manage.py populate_posts
```

Creates demo user (username: demo, password: demo123) with 50 sample posts.

## Project Structure

```
Django-Blog-Application/
├── account/                    # User auth and profiles
├── post/                       # Blog posts
├── core/                       # Settings and config
├── templates/                  # HTML templates
│   ├── account/               # Auth templates
│   ├── post/                  # Post templates
│   ├── registration/          # Email templates
│   └── partials/              # Shared components
├── static/                     # CSS and static files
├── media/                      # User uploads
├── db.sqlite3                  # Database
├── .env.example                # Configuration template
└── manage.py                   # Django management script
```

## Security

1. Generate unique `SECRET_KEY` for each environment
2. Never commit `.env` files with real credentials
3. Use strong database passwords
4. Enable HTTPS in production
5. Keep dependencies updated
6. Use environment variables for sensitive data

## Troubleshooting

**Emails not working:**
```bash
# Check .env configuration
cat .env | grep EMAIL
# Verify with test:
python manage.py shell
# Then: from django.core.mail import send_mail; send_mail('Test', 'Body', 'from@example.com', ['to@example.com'])
```

**Database errors:**
```bash
python manage.py migrate
# Or reset: rm db.sqlite3 && python manage.py migrate
```

**Port already in use:**
```bash
python manage.py runserver 8001
```

**Static files missing:**
```bash
python manage.py collectstatic
```

## Deployment

1. Copy `.env.example` to `.env`
2. Edit `.env` with environment-specific values
3. Run migrations: `python manage.py migrate`
4. Collect static files: `python manage.py collectstatic`

**Development:**
```bash
python manage.py runserver
```

**Production:**
```bash
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## Docker Setup

### Prerequisites

- Docker
- Docker Compose

### Quick Start with Docker

```bash
chmod +x docker.sh

# Start application
./docker.sh up

# Stop application
./docker.sh down

# View logs
./docker.sh logs

# Run migrations
./docker.sh migrate

# Access shell
./docker.sh shell

# Run bash
./docker.sh bash
```

### Docker Commands Reference

| Command | Description |
|---------|-------------|
| `./docker.sh up` | Start containers and run migrations |
| `./docker.sh down` | Stop all containers |
| `./docker.sh logs` | View container logs |
| `./docker.sh test` | Run tests |
| `./docker.sh shell` | Django shell |
| `./docker.sh bash` | Container bash shell |
| `./docker.sh migrate` | Run migrations |
| `./docker.sh makemigrations` | Create migrations |
| `./docker.sh static` | Collect static files |

### Docker Services

- **web**: Django application (port 8000)
- **db**: PostgreSQL database (port 5432)

## Testing

### Run Tests

```bash
# Django tests
python manage.py test

# Pytest
pytest

# Coverage report
pytest --cov=. --cov-report=html
```

### Test Files

- `account/tests.py` - Authentication tests
- `post/tests_models.py` - Post model tests
- `post/tests_views.py` - Post view tests

### Test Coverage

Tests cover:
- User registration and login
- Post creation, editing, deletion
- Password reset functionality
- Permission checks
- View responses and redirects

## Verification

```bash
python manage.py check
```


## License

MIT License - see LICENSE file for details

## Implementation Summary

### New Features Added

1. **Comprehensive Testing Suite**
   - 23 unit tests covering authentication, models, and views
   - Test coverage for user registration, login, and password reset
   - Post CRUD operation tests
   - Permission and authorization tests
   - All tests passing

2. **Docker Support**
   - Dockerfile for containerized application
   - docker-compose.yml with PostgreSQL and Django services
   - docker.sh helper script for common operations
   - .dockerignore for optimized builds

3. **Production Ready**
   - Gunicorn WSGI server
   - PostgreSQL database support
   - Environment-based configuration
   - Static file collection support

4. **Development Tools**
   - pytest and pytest-django for testing
   - Coverage reporting
   - pytest.ini configuration

### Files Created

```
Dockerfile                    # Container configuration
docker-compose.yml           # Multi-container setup
docker.sh                    # Helper script
.dockerignore               # Docker ignore file
pytest.ini                  # Test configuration
.env.docker                 # Docker environment example
post/tests_models.py        # Post model tests
post/tests_views.py         # Post view tests
```

### Files Updated

```
requirements.txt            # Added testing and production packages
README.md                   # Added Docker and testing documentation
account/tests.py            # Added authentication tests
settings.py                 # Environment variable support
```

### Test Coverage

- Authentication (8 tests)
  - Registration page
  - Login page
  - User registration
  - User login
  - User logout
  - Profile access
  - Password reset page
  - Invalid login handling

- Post Models (4 tests)
  - Post creation
  - String representation
  - Ordering
  - Absolute URL

- Post Views (11 tests)
  - Index view
  - Post detail view
  - Posts list view
  - User posts view
  - Create post authentication
  - Create post form submission
  - Edit post authorization
  - Delete post functionality

### Quick Commands

**Development:**
```bash
python manage.py runserver
python manage.py test
pytest
```

**Docker:**
```bash
chmod +x docker.sh
./docker.sh up           # Start containers
./docker.sh down         # Stop containers
./docker.sh test         # Run tests
./docker.sh logs         # View logs
```

**Production:**
```bash
docker build -t blog-app .
docker run -p 8000:8000 blog-app
```

### Technology Stack

- Django 6.0.3
- PostgreSQL 15 (Docker)
- Bootstrap 5
- Gunicorn
- Python 3.14

### Next Steps

1. Deploy to production server
2. Configure real SMTP provider (Gmail, SendGrid, etc.)
3. Set up CI/CD pipeline
4. Configure SSL/TLS
5. Add monitoring and logging

All tests passing and ready for deployment!



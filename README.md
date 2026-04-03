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
# Make script executable
chmod +x docker.sh

# Start application (pulls images, builds, migrates, and starts services)
./docker.sh up

# The application will be available at http://localhost:8000
# Create superuser when prompted

# View logs
./docker.sh logs

# Stop application
./docker.sh down
```

### Available Docker Commands

```bash
./docker.sh up              # Start containers and run migrations
./docker.sh down            # Stop all containers
./docker.sh logs            # View container logs in real-time
./docker.sh test            # Run test suite
./docker.sh shell           # Access Django shell
./docker.sh bash            # Access container bash
./docker.sh migrate         # Run migrations
./docker.sh makemigrations  # Create new migrations
./docker.sh static          # Collect static files
```

### Docker Services

| Service | Port | Details |
|---------|------|---------|
| web | 8000 | Django development server |
| db | 5432 | PostgreSQL 15 database |

### Database

- PostgreSQL 15
- Database: blog_db
- User: blog_user
- Password: blog_password (change in production!)

### Troubleshooting

**Port already in use:**
```bash
# Stop existing containers
./docker.sh down

# Or use different port (edit docker-compose.yml)
ports:
  - "8001:8000"  # Use 8001 instead
```

**Database connection error:**
```bash
# Ensure db service is healthy
docker-compose ps

# Check logs
./docker.sh logs
```

**Clean rebuild:**
```bash
./docker.sh down
docker-compose build --no-cache
./docker.sh up
```

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

### Next Steps

1. Deploy to production server
2. Set up CI/CD pipeline
3. Configure SSL/TLS
4. Add monitoring and logging

## License

MIT License - see LICENSE file for details

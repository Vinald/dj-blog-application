# Django Blog Application

A modern, feature-rich Django blog application with user authentication, post management, images, tags, comments, and
password reset functionality.

## Features

### Core Features

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
- Django admin panel for managing posts, users, and comments
- Django sessions to track recently viewed posts and page visit statistics
- **Featured Images** - Upload and display post images
- **Tags** - Organize posts with multiple tags
- **Comments** - Full comment system with moderation

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
DEBUG=True

# Database Configuration (PostgreSQL)
DB_NAME=blog_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_CONN_MAX_AGE=600
DB_SSLMODE=prefer
```

**Production:**

```
SECRET_KEY=generate-new-key
DEBUG=False
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourblog.com
PASSWORD_RESET_TIMEOUT=3600

# Database Configuration (PostgreSQL)
DB_NAME=blog_db
DB_USER=blog_user
DB_PASSWORD=your_very_secure_password
DB_HOST=your-db-host.com
DB_PORT=5432
DB_CONN_MAX_AGE=600
DB_SSLMODE=require

# Cloud Deployment (Alternative - use instead of DB_* variables)
# DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Variables

| Variable                 | Purpose                                                                                                                                         |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `SECRET_KEY`             | Django secret key (generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`) |
| `DEBUG`                  | `False` for production, `True` for development                                                                                                  |
| `EMAIL_BACKEND`          | `django.core.mail.backends.console.EmailBackend` (dev) or `django.core.mail.backends.smtp.EmailBackend` (production)                            |
| `EMAIL_HOST`             | SMTP server (e.g., smtp.gmail.com)                                                                                                              |
| `EMAIL_PORT`             | SMTP port (usually 587)                                                                                                                         |
| `EMAIL_USE_TLS`          | True or False                                                                                                                                   |
| `EMAIL_HOST_USER`        | SMTP username                                                                                                                                   |
| `EMAIL_HOST_PASSWORD`    | SMTP password or app password                                                                                                                   |
| `DEFAULT_FROM_EMAIL`     | Sender email address                                                                                                                            |
| `PASSWORD_RESET_TIMEOUT` | Reset link validity in seconds (3600 = 1 hour)                                                                                                  |
| `DB_NAME`                | PostgreSQL database name (default: `blog_db`)                                                                                                   |
| `DB_USER`                | PostgreSQL user (default: `postgres`)                                                                                                           |
| `DB_PASSWORD`            | PostgreSQL password (default: `postgres`)                                                                                                       |
| `DB_HOST`                | PostgreSQL host (default: `localhost`)                                                                                                          |
| `DB_PORT`                | PostgreSQL port (default: `5432`)                                                                                                               |
| `DB_CONN_MAX_AGE`        | Connection pooling timeout in seconds (default: `600`)                                                                                          |
| `DB_SSLMODE`             | SSL mode: `disable`, `allow`, `prefer`, or `require` (use `require` in production)                                                              |
| `DATABASE_URL`           | Alternative to DB_* variables for cloud deployments (Heroku, Docker, Railway)                                                                  |

### Security

- **Never commit `.env` file** - Only `.env.example` should be in git
- **Development:** Emails print to console - no provider needed
- **Production:** Use real SMTP provider and enable security settings
- **Database:** Use strong passwords and SSL mode `require` in production
- **Credentials:** Store sensitive values in environment variables, never in code

### Database Setup (PostgreSQL)

#### Installation

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Docker:**
```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:latest
```

#### Create Database and User

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE blog_db;
CREATE USER blog_user WITH PASSWORD 'secure_password';
ALTER ROLE blog_user SET client_encoding TO 'utf8';
ALTER ROLE blog_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE blog_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE blog_db TO blog_user;
\q
```

#### Run Migrations

```bash
python3 manage.py migrate
```

#### Test Database Connection

```bash
python3 manage.py dbshell
```

### Database Configuration Details

**Connection Pooling:**
- `DB_CONN_MAX_AGE=600` reuses database connections
- Improves performance by reducing connection overhead
- Closes idle connections after 600 seconds

**SSL Modes:**
- `disable` - No SSL (development only)
- `allow` - SSL attempted but not required
- `prefer` - SSL preferred if available (development)
- `require` - SSL required (production recommended)

**Cloud Deployment Options:**

1. **Heroku:** Uses `DATABASE_URL` automatically
2. **Railway:** Set `DATABASE_URL` in environment
3. **Docker:** Use `DATABASE_URL` or individual `DB_*` variables
4. **Self-hosted:** Use individual `DB_*` variables

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

### Featured Images

- **Upload:** When creating/editing a post, click "Choose Image" to upload a featured image
- **Display:** Image appears full-width at top of post detail page
- **Thumbnails:** Image shows as thumbnail on post listing pages (responsive)
- **Optional:** Posts work perfectly fine without images
- **Storage:** Images stored in `media/post_images/` directory

### Tags

**Admin Management:**

1. Go to `/admin/post/tag/`
2. Click "Add Tag"
3. Enter tag title (e.g., "Django", "Python", "Web Dev")
4. Slug auto-generates from title
5. Click Save

**Using Tags on Posts:**

1. When creating/editing a post
2. Check desired tags in "Tags" section
3. Multiple tags per post allowed
4. Tags saved with post automatically
5. Tags display as badges on all post views

**Features:**

- Filter posts by tags in admin
- Search tags in admin
- View post count per tag
- Tags display on post detail and listings

### Comments

**Posting Comments:**

1. Go to any post's detail page
2. Scroll to "Comments" section
3. If logged in: Fill comment form and click "Post Comment"
4. If not logged in: Click login link to authenticate
5. Comment appears immediately

**Managing Comments:**

- **Delete own:** Click "Delete" on your comments
- **Post author:** Can delete any comment on their posts
- **Admin:** Full comment management at `/admin/post/comment/`

**Features:**

- Comment count displayed on post listings
- Comments ordered by newest first
- Author name and timestamp shown
- Form validates input
- Success/error messages display

### Admin Panel

Access at: http://localhost:8000/admin/

**Enhanced Admin Features:**

- **Posts:** View comment count and tags per post
- **Tags:** See how many posts use each tag
- **Comments:** Full management with filtering and search
- **Inline comments:** Manage comments while editing posts

## Usage Examples

### Creating a Post with Image and Tags

```bash
1. Click "New Post"
2. Fill in Title, Slug, Content
3. Click "Choose Image" and upload a featured image
4. Check desired tags (Django, Python, etc.)
5. Click "Publish Post"
```

### Commenting on a Post

```bash
1. Navigate to post detail page
2. Scroll to "Comments" section
3. Fill in comment form
4. Click "Post Comment"
5. Comment appears immediately
```

### Managing Tags

```bash
# Create tags (admin only)
Go to /admin/post/tag/ → Add Tag

# Select tags on post
When creating/editing → check desired tags

# View tag statistics
Go to /admin/post/tag/ → see post count per tag
```

## Testing

### Test Coverage Summary

The application includes **116 comprehensive tests** covering:

#### Account App Tests (40 tests)
- **Authentication:** Registration, login, logout, password reset
- **Profile Management:** Profile viewing, editing, bio, name, email
- **Form Validation:** Duplicate detection, password matching, field validation
- **Permissions:** Login requirements, access control
- **Profile Model:** Relationships, cascading deletes, field validation

#### Post App Tests (76 tests)
- **Post CRUD:** Create, read, update, delete with proper permissions
- **Comments:** Create, delete, permissions, ordering
- **Tags:** Creation, relationships, multiple tags per post
- **Views:** Index, about, posts list, user posts, post detail
- **Permissions:** Owner-only operations, non-owner access denial
- **Models:** Relationships, cascade deletes, auto-timestamps
- **Forms:** Validation, error handling, tag selection

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test account.tests
python manage.py test account.tests_models
python manage.py test post.tests_models
python manage.py test post.tests_views

# Run specific test class
python manage.py test account.tests.AccountAuthTests
python manage.py test post.tests_views.PostViewTests

# Run specific test method
python manage.py test account.tests.AccountAuthTests.test_user_login_valid

# Run with verbose output
python manage.py test --verbosity=2

# Run with coverage report
coverage run --source='.' manage.py test
coverage report
coverage html  # Creates htmlcov/index.html
```

### Test Files

- `account/tests.py` - 31 authentication & profile tests
- `account/tests_models.py` - 9 profile model tests (NEW)
- `post/tests_models.py` - 27 post & comment model tests
- `post/tests_views.py` - 49 post & comment view tests

### Test Results

✅ **Status:** All 116 tests passing  
✅ **Coverage:** Account & Post apps fully tested  
✅ **Production Ready:** Yes

### Images Feature

**Backend:**

- Image field added to Post model (`image = ImageField(upload_to='post_images/', null=True, blank=True)`)
- Image upload field in post creation/editing forms
- Optional field - posts work without images

**Frontend:**

- Featured image displays full-width at top of post detail page
- Image thumbnails show on post listing pages (responsive grid)
- Graceful fallback for posts without images
- Images optimized for different screen sizes (mobile, tablet, desktop)

**Admin:**

- Image preview in post admin form
- See image in post list view
- Can replace image when editing posts

### Tags Feature

**Backend:**

- Tag model created with title and slug
- Many-to-Many relationship with Post model
- Auto-slug generation from title
- Tags ordered alphabetically

**Frontend:**

- Tag selection via checkboxes when creating/editing posts
- Tags display as Bootstrap badges on all post views
- Multiple tags per post supported
- Tags visible on: post detail, home page, posts list, user posts

**Admin:**

- Full TagAdmin interface at `/admin/post/tag/`
- Create, edit, delete tags
- View post count per tag
- Search tags by title
- Auto-slug generation

### Comments Feature

**Backend:**

- Comment model with post and author foreign keys
- CreateCommentView - authenticated users can post comments
- DeleteCommentView - users can delete own comments, post authors can moderate all
- Comment timestamps (created_at, updated_at)
- Comments ordered by newest first

**Frontend:**

- Comments section on post detail page
- Comment count displayed on post listings
- Comment form for logged-in users
- Login prompt for anonymous users
- Author name and timestamp on each comment
- Delete button for comment author or post author

**Admin:**

- Full CommentAdmin interface at `/admin/post/comment/`
- Filter by post or date
- Search by author, content, or post
- View comment preview (100 chars)
- Delete comments
- Inline comment management in post editor

**Security:**

- Login required to comment
- Users can only delete own comments
- Post authors can delete any comment on their posts
- CSRF protection on all forms
- Form validation and error handling

### Database Changes

**New Tables:**

- `post_tag` - Tag definitions
- `post_comment` - Reader comments
- `post_post_tags` - Post-Tag many-to-many relationships

**New Fields:**

- `post.image` - Featured image file path
- `post.tags` - M2M relationship to tags

**Migration:**

- File: `post/migrations/0004_tag_post_image_alter_post_author_comment_post_tags.py`
- Status: Applied automatically on `python manage.py migrate`

### Code Structure

**Models** (`post/models.py`):

- `Tag` - Tag model with title, slug, ordering
- `Post` - Enhanced with image field and tags M2M
- `Comment` - New comment model

**Forms** (`post/forms.py`):

- `PostForm` - Enhanced with image and tags fields
- `CommentForm` - New comment form

**Views** (`post/views.py`):

- `PostDetailView` - Enhanced with comments and comment form
- `CreateCommentView` - New view for posting comments
- `DeleteCommentView` - New view for deleting comments

**Admin** (`post/admin.py`):

- `PostAdmin` - Enhanced with comment inline, tag filter
- `TagAdmin` - New admin interface for tags
- `CommentAdmin` - New admin interface for comments

**URLs** (`post/urls.py`):

- `/posts/<slug>/comment/` - POST comment
- `/posts/<slug>/comment/<id>/delete/` - DELETE comment

**Templates** (6 updated):

- `post_detail.html` - Full comments section + featured image
- `index.html` - Image thumbnails + comment count
- `posts.html` - Image thumbnails + comment count
- `user_posts.html` - Image thumbnails + comment count
- `create_post.html` - Image upload + tags selection
- `edit_post.html` - Image preview + tags editing

### Troubleshooting

**Images not showing:**

```bash
# Check media directory exists
ls -la media/post_images/

# Verify MEDIA_ROOT and MEDIA_URL in settings
grep MEDIA_ core/settings.py

# Restart dev server
python manage.py runserver
```

**Tags not appearing:**

```bash
# Verify tags created in admin
python manage.py shell
>>> from post.models import Tag
>>> Tag.objects.all()

# Verify M2M relationship
>>> from post.models import Post
>>> post = Post.objects.first()
>>> post.tags.all()
```

**Comments not working:**

```bash
# Check logged in to post comments
# Verify database has comment table
python manage.py migrate

# Check admin interface
# Visit /admin/post/comment/
```

**Template errors:**

```bash
# Run Django check
python manage.py check

# Clear template cache
# Restart dev server
python manage.py runserver
```

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

## Testing

Create sample data:

```bash
python manage.py populate_posts
```

Creates demo user (username: demo, password: demo123) with 50 sample posts.

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

### Docker Troubleshooting

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

**Migration errors (e.g., "relation already exists"):**

```bash
# Option 1: Fake initial migration (recommended for development)
docker-compose exec web python manage.py migrate --fake-initial

# Option 2: Use database reset script
chmod +x reset_db.sh
./reset_db.sh
```

**Using the database reset script:**

The `reset_db.sh` script provides an interactive menu to:
- Reset database completely (fresh start, destroys all data)
- Fake initial migration (skip 0001_initial if tables exist)
- Show migration status
- Run migrations manually

**Clean rebuild:**

```bash
./docker.sh down
docker-compose build --no-cache
./docker.sh up
```

## License

MIT License - see LICENSE file for details

## Django Sessions Implementation

### Overview

This project includes a comprehensive session management system to track user behavior and preferences.

### Session Configuration

```python
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Store in database
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_SECURE = not DEBUG  # HTTPS only in production
SESSION_COOKIE_HTTPONLY = True  # Protect from JS access
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Persist after browser closes
SESSION_SAVE_EVERY_REQUEST = False  # Save only when modified (efficient)
```

### Session Features

#### 1. Recently Viewed Posts Tracking

- **Location**: `PostDetailView.get()` in `post/views.py`
- **Description**: Tracks last 5 posts viewed by user
- **Session Key**: `recently_viewed`
- **Data Structure**: List of post IDs in order of viewing (most recent first)

**Usage in templates:**

```django
{% for post in recently_viewed_posts %}
    {{ post.title }}
{% endfor %}
```

**Template partial:** `templates/partials/recently_viewed.html`

#### 2. Page Visit Statistics

- **Location**: `IndexView.get()` in `post/views.py`
- **Description**: Counts page visits per session
- **Session Key**: `page_visits`
- **Data Structure**: Dictionary with page names and visit counts

**Example session data:**

```python
{
    'recently_viewed': ['5', '3', '1'],
    'page_visits': {
        'home_page': 42
    }
}
```

#### 3. Context Processor

- **File**: `post/context_processors.py`
- **Function**: `session_processor(request)`
- **Purpose**: Makes recently viewed posts available to all templates
- **Returns**: 
  - `recently_viewed_posts`: List of actual Post objects (not just IDs)
  - `page_visits`: Dictionary of page visit counts

#### 4. Session Management

- **Endpoint**: `/account/sessions/clear/`
- **Method**: POST
- **View**: `ClearSessionsView` in `account/session_views.py`
- **Purpose**: Allows users to clear their session data
- **Clears**: `recently_viewed`, `page_visits`

### Using Sessions in Your Code

#### Reading Session Data

```python
def my_view(request):
    recently_viewed = request.session.get('recently_viewed', [])
    page_visits = request.session.get('page_visits', {})
```

#### Writing Session Data

```python
def my_view(request):
    # Add data
    request.session['my_data'] = 'value'
    
    # Mark as modified (only needed for mutable data)
    request.session.modified = True
    
    # Delete data
    del request.session['my_data']
```

#### Session Methods

```python
request.session.flush()  # Delete entire session
request.session.cycle_key()  # Create new session ID (security)
request.session.clear()  # Delete all session data
```

### Security Best Practices

✅ **Implemented:**

- `SESSION_COOKIE_HTTPONLY = True` - JavaScript can't access
- `SESSION_COOKIE_SAMESITE = 'Lax'` - CSRF protection
- `SESSION_COOKIE_SECURE = not DEBUG` - HTTPS only in production
- Database backend - more secure than files

✅ **For Production:**

Use Redis or Memcached for sessions (faster):

```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Common Use Cases

#### Remember Search Filters

```python
request.session['search_query'] = query
request.session['filter_tags'] = tags
request.session.modified = True
```

#### Shopping Cart (E-commerce)

```python
request.session['cart'] = {
    'item_1': {'qty': 2, 'price': 19.99},
    'item_2': {'qty': 1, 'price': 29.99}
}
```

#### Wizard/Multi-step Forms

```python
request.session['form_step'] = 2
request.session['form_data'] = {'field1': 'value1'}
```

### Database Management

Sessions are stored in `django_session` table:

```bash
# Clean up expired sessions (run regularly in production)
python manage.py clearsessions
```

Add to cron job for production:

```bash
0 0 * * * python /path/to/manage.py clearsessions
```

### Viewing Session Data in Admin

1. Login to Django admin
2. Navigate to Sessions table
3. View session key, data, and expiry date

### Testing Sessions

```python
# In tests
def test_session_tracking(client):
    response = client.get('/post/slug-1/')
    assert 'recently_viewed' in client.session
    assert '1' in client.session['recently_viewed']
```

### Performance Considerations

- ✅ `SESSION_SAVE_EVERY_REQUEST = False` - Only saves when modified
- ✅ Database backend - Good for small-medium projects
- 🔄 For high-traffic sites, migrate to Redis/Memcached
- 🧹 Run `clearsessions` command regularly to remove expired sessions

### Troubleshooting Sessions

**Sessions not persisting?**

- Check `SESSION_COOKIE_SECURE = True` on HTTPS
- Verify middleware order: SessionMiddleware must be before AuthenticationMiddleware

**Sessions cleared unexpectedly?**

- Check `SESSION_EXPIRE_AT_BROWSER_CLOSE` setting
- Review `SESSION_COOKIE_AGE` timeout

**Performance issues?**

- Switch to Redis/Memcached backend
- Run `clearsessions` command to clean up database



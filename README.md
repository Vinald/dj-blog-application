# Django Blog Application

A modern, feature-rich Django blog application with user authentication, post management, images, tags, comments, and
password reset functionality.

## ✨ Features

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

### 🆕 Enhanced Features (April 2026)

- **📸 Featured Images** - Upload and display post images
- **🏷️ Tags** - Organize posts with multiple tags
- **💬 Comments** - Full comment system with moderation

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

| Variable                 | Purpose                                                                                                                                         |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `SECRET_KEY`             | Django secret key (generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`) |
| `EMAIL_BACKEND`          | `django.core.mail.backends.console.EmailBackend` (dev) or `django.core.mail.backends.smtp.EmailBackend` (production)                            |
| `EMAIL_HOST`             | SMTP server (e.g., smtp.gmail.com)                                                                                                              |
| `EMAIL_PORT`             | SMTP port (usually 587)                                                                                                                         |
| `EMAIL_USE_TLS`          | True or False                                                                                                                                   |
| `EMAIL_HOST_USER`        | SMTP username                                                                                                                                   |
| `EMAIL_HOST_PASSWORD`    | SMTP password or app password                                                                                                                   |
| `DEFAULT_FROM_EMAIL`     | Sender email address                                                                                                                            |
| `PASSWORD_RESET_TIMEOUT` | Reset link validity in seconds (3600 = 1 hour)                                                                                                  |

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

### 💬 Comments

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

Create sample data:

```bash
python manage.py populate_posts
```

Creates demo user (username: demo, password: demo123) with 50 sample posts.

## New Features Documentation (April 2026)

### 📸 Images Feature

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

### 🏷️ Tags Feature

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

## License

MIT License - see LICENSE file for details

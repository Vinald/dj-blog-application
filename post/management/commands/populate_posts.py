from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from post.models import Post
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Insert 50 sample blog posts into the database'

    def handle(self, *args, **options):
        # Get or create a default user
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )

        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))

        # Sample post titles and content
        titles = [
            'Getting Started with Django',
            'Introduction to Python Web Development',
            'Building RESTful APIs with Django',
            'Django Models and Databases',
            'Authentication and Authorization in Django',
            'Class-Based Views vs Function-Based Views',
            'Django ORM: A Complete Guide',
            'Creating Custom Django Middleware',
            'Django Forms and Validation',
            'Building Real-time Applications with Django',
            'Django Testing Best Practices',
            'Performance Optimization in Django',
            'Django Admin Customization',
            'Celery and Task Queues in Django',
            'Django Security Best Practices',
            'Building Multi-Tenant Applications',
            'Docker and Django Deployment',
            'CI/CD Pipelines for Django',
            'Django REST Framework Tutorial',
            'GraphQL with Django',
            'WebSocket Integration in Django',
            'Caching Strategies in Django',
            'Database Optimization Techniques',
            'Building Scalable Django Applications',
            'API Rate Limiting in Django',
            'User Authentication with OAuth',
            'File Upload Handling in Django',
            'Email Integration in Django',
            'Django Signals Explained',
            'Creating Django Packages',
            'Managing Static and Media Files',
            'Django Middleware Deep Dive',
            'Building Chat Applications',
            'Data Serialization in Django',
            'Query Optimization with Django',
            'Building Mobile APIs',
            'Django Pagination Techniques',
            'Search Functionality Implementation',
            'Versioning APIs in Django',
            'Error Handling Best Practices',
            'Building Admin Dashboards',
            'Django Logging Configuration',
            'Building E-commerce Platforms',
            'Payment Integration in Django',
            'Building Social Media Features',
            'Django Internationalization',
            'Building Microservices with Django',
            'Testing Database Models',
            'Advanced QuerySet Operations',
            'Building Data Analytics Dashboards',
        ]

        content_template = '''This is an in-depth article about {title}.

In this post, we'll explore the key concepts, best practices, and implementation details you need to know to master this topic.

Key Topics Covered:
- Introduction and overview
- Core concepts and fundamentals
- Practical implementation examples
- Best practices and tips
- Common pitfalls and how to avoid them
- Advanced techniques
- Real-world use cases
- Performance considerations
- Security implications
- Testing strategies

Whether you're a beginner or an experienced developer, this guide will help you understand and implement {topic} effectively in your Django projects.

The examples provided are production-ready and follow industry best practices. You can use them as a starting point for your own implementations.

For more information and updates, make sure to follow our blog and subscribe to our newsletter. Happy coding!'''

        # Create posts
        created_count = 0
        for i, title in enumerate(titles, 1):
            slug = slugify(title) + f'-{i}'

            # Check if post already exists
            if Post.objects.filter(slug=slug).exists():
                self.stdout.write(self.style.WARNING(f'Post with slug "{slug}" already exists, skipping...'))
                continue

            content = content_template.format(
                title=title,
                topic=title.lower()
            )

            post = Post.objects.create(
                title=title,
                slug=slug,
                content=content,
                author=user
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'✓ Created post: {title}'))

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully created {created_count} posts!')
        )


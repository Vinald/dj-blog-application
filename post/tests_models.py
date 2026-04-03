from django.test import TestCase
from django.contrib.auth.models import User
from post.models import Post


class PostModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_post_creation(self):
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertTrue(post.slug)

    def test_post_str_representation(self):
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user
        )
        self.assertEqual(str(post), 'Test Post')

    def test_post_ordering(self):
        post1 = Post.objects.create(
            title='First Post',
            slug='first-post',
            content='Content 1',
            author=self.user
        )
        post2 = Post.objects.create(
            title='Second Post',
            slug='second-post',
            content='Content 2',
            author=self.user
        )
        posts = Post.objects.all()
        self.assertEqual(posts[0], post2)
        self.assertEqual(posts[1], post1)

    def test_post_get_absolute_url(self):
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user
        )
        self.assertEqual(post.get_absolute_url(), f'/posts/{post.slug}/')


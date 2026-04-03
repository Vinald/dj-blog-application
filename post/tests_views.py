from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from post.models import Post


class PostViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'This is test content')

    def test_posts_list_view(self):
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_user_posts_view(self):
        response = self.client.get(reverse('user_posts', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_create_post_requires_login(self):
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/account/login/', response.url)

    def test_create_post_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)

    def test_create_post_post_request(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('create_post'), {
            'title': 'New Post',
            'slug': 'new-post',
            'content': 'New content'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_edit_post_own_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit_post', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)

    def test_edit_post_not_owner(self):
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('edit_post', args=[self.post.slug]))
        self.assertEqual(response.status_code, 302)

    def test_delete_post_own_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('delete_post', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)

    def test_delete_post_post_request(self):
        self.client.login(username='testuser', password='testpass123')
        post_slug = self.post.slug
        response = self.client.post(reverse('delete_post', args=[post_slug]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(slug=post_slug).exists())


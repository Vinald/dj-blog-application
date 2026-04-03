from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AccountAuthTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_register_page_loads(self):
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        response = self.client.post(reverse('account:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123!@#',
            'password2': 'newpass123!@#'
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        response = self.client.post(reverse('account:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_user_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account:logout'))
        self.assertEqual(response.status_code, 200)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_loads_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_page(self):
        response = self.client.get(reverse('account:password_reset'))
        self.assertEqual(response.status_code, 200)

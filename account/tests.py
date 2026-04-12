from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from account.models import Profile


class AccountAuthTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    # Registration Tests
    def test_register_page_loads(self):
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_register_page_redirects_authenticated_user(self):
        """Authenticated users should be redirected from register page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_user_registration_valid(self):
        """Test successful user registration"""
        response = self.client.post(reverse('account:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123!@#',
            'password2': 'newpass123!@#'
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:login'))

    def test_user_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        response = self.client.post(reverse('account:register'), {
            'username': 'testuser',
            'email': 'another@example.com',
            'password1': 'newpass123!@#',
            'password2': 'newpass123!@#'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_user_registration_duplicate_email(self):
        """Test registration with duplicate email"""
        response = self.client.post(reverse('account:register'), {
            'username': 'newuser',
            'email': 'test@example.com',
            'password1': 'newpass123!@#',
            'password2': 'newpass123!@#'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_user_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        response = self.client.post(reverse('account:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123!@#',
            'password2': 'wrongpass123!@#'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_user_registration_weak_password(self):
        """Test registration with weak password"""
        response = self.client.post(reverse('account:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': '123',
            'password2': '123'
        })
        self.assertEqual(response.status_code, 200)

    def test_registration_creates_profile(self):
        """Test that registering a user creates a profile"""
        self.client.post(reverse('account:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123!@#',
            'password2': 'newpass123!@#'
        })
        new_user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertIsNotNone(new_user.profile)

    # Login Tests
    def test_login_page_loads(self):
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_login_page_redirects_authenticated_user(self):
        """Authenticated users should be redirected from login page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_user_login_valid(self):
        """Test successful user login"""
        response = self.client.post(reverse('account:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_user_login_invalid_password(self):
        """Test login with invalid password"""
        response = self.client.post(reverse('account:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_user_login_nonexistent_user(self):
        """Test login with non-existent user"""
        response = self.client.post(reverse('account:login'), {
            'username': 'nonexistent',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_user_login_with_next_parameter(self):
        """Test login with next parameter redirects to next page"""
        response = self.client.post(reverse('account:login') + '?next=/posts/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/posts/')

    # Logout Tests
    def test_user_logout_page_requires_login(self):
        """Logout page should require login"""
        response = self.client.get(reverse('account:logout'))
        self.assertEqual(response.status_code, 302)

    def test_user_logout_get_request(self):
        """Test logout page GET request shows confirmation"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/logout.html')

    def test_user_logout_post_request(self):
        """Test logout POST request logs out user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('account:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        # User should be logged out
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 302)

    # Profile Tests
    def test_profile_requires_login(self):
        """Profile page should require login"""
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_loads_authenticated(self):
        """Profile page should load for authenticated users"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')

    def test_profile_context_data(self):
        """Test profile page context contains correct data"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['profile'], self.user.profile)

    def test_profile_display_user_info(self):
        """Test profile page displays user information"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account:profile'))
        self.assertContains(response, 'testuser')

    # Edit Profile Tests
    def test_edit_profile_requires_login(self):
        """Edit profile page should require login"""
        response = self.client.get(reverse('account:edit_profile'))
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_loads_authenticated(self):
        """Edit profile page should load for authenticated users"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/edit_profile.html')

    def test_edit_profile_update_email(self):
        """Test updating email in profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('account:edit_profile'), {
            'username': 'testuser',
            'email': 'newemail@example.com',
            'first_name': '',
            'last_name': '',
            'bio': ''
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_edit_profile_update_bio(self):
        """Test updating bio in profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('account:edit_profile'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': '',
            'last_name': '',
            'bio': 'This is my bio'
        })
        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'This is my bio')

    def test_edit_profile_update_full_name(self):
        """Test updating first and last name in profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('account:edit_profile'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'bio': ''
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')

    def test_edit_profile_duplicate_email(self):
        """Test edit profile with duplicate email fails"""
        other_user = User.objects.create_user(
            username='otheruser2',
            email='other@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('account:edit_profile'), {
            'username': 'testuser',
            'email': 'other@example.com',
            'first_name': '',
            'last_name': '',
            'bio': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_form', response.context)
        self.assertTrue(response.context['user_form'].errors)

    def test_edit_profile_duplicate_username(self):
        """Test edit profile with duplicate username fails"""
        other_user = User.objects.create_user(
            username='otheruser3',
            email='other3@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('account:edit_profile'), {
            'username': 'otheruser3',
            'email': 'test@example.com',
            'first_name': '',
            'last_name': '',
            'bio': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_form', response.context)
        self.assertTrue(response.context['user_form'].errors)

    # Password Reset Tests
    def test_password_reset_page_loads(self):
        """Password reset page should be accessible"""
        response = self.client.get(reverse('account:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_reset.html')

    def test_password_reset_with_valid_email(self):
        """Test password reset with valid email"""
        response = self.client.post(reverse('account:password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)

    def test_password_reset_with_invalid_email(self):
        """Test password reset with non-existent email"""
        response = self.client.post(reverse('account:password_reset'), {
            'email': 'nonexistent@example.com'
        })
        # Should still return 302 for security reasons (don't reveal if email exists)
        self.assertEqual(response.status_code, 302)

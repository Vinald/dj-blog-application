from django.test import TestCase
from django.contrib.auth.models import User
from account.models import Profile
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


class ProfileModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_profile_created_for_new_user(self):
        """Test that a profile is created when a new user is registered"""
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='testpass123'
        )
        self.assertTrue(hasattr(new_user, 'profile'))

    def test_profile_str_representation(self):
        """Test the string representation of Profile"""
        profile = self.user.profile
        self.assertEqual(str(profile), f'{self.user.username} Profile')

    def test_profile_default_image(self):
        """Test that profile has default image"""
        profile = self.user.profile
        self.assertEqual(profile.image.name, 'default.jpg')

    def test_profile_bio_field(self):
        """Test that profile bio field can be set"""
        profile = self.user.profile
        profile.bio = 'This is my bio'
        profile.save()
        profile.refresh_from_db()
        self.assertEqual(profile.bio, 'This is my bio')

    def test_profile_bio_can_be_empty(self):
        """Test that profile bio can be empty"""
        profile = self.user.profile
        profile.bio = ''
        profile.save()
        profile.refresh_from_db()
        self.assertEqual(profile.bio, '')

    def test_profile_one_to_one_relationship(self):
        """Test that each user has exactly one profile"""
        profile1 = self.user.profile
        profile2 = self.user.profile
        self.assertEqual(profile1.id, profile2.id)

    def test_profile_user_cascade_delete(self):
        """Test that profile is deleted when user is deleted"""
        profile_id = self.user.profile.id
        self.user.delete()
        self.assertFalse(Profile.objects.filter(id=profile_id).exists())

    def test_profile_user_relationship(self):
        """Test that profile can access its user"""
        profile = self.user.profile
        self.assertEqual(profile.user, self.user)

    def test_profile_multiple_users_different_profiles(self):
        """Test that different users have different profiles"""
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        profile1 = self.user.profile
        profile2 = user2.profile
        self.assertNotEqual(profile1.id, profile2.id)
        self.assertNotEqual(profile1.user, profile2.user)


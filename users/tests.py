from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileTest(TestCase):
    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)
        profile = user.userprofile
        self.assertEqual(profile.user, user)

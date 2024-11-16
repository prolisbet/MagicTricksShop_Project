from django.test import TestCase
from .models import User
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MagicTricksShop.settings')
django.setup()


class UserModelTest(TestCase):
    def setUp(self):
        User.objects.create(name="testuser", email="testuser@example.com")

    def test_user_creation(self):
        user = User.objects.get(name="testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_string_representation(self):
        user = User.objects.get(name="testuser")
        self.assertEqual(str(user), "testuser")

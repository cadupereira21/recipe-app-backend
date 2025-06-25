"""We are going to use TestCase since it has built-in support for database transactions and rollbacks. Because of
that, it is considerably slower than SimpleTestCase, since it has a database setup overhead, but it is more suitable for testing models that interact with
the database."""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email=email, password=password)


class TestModels(TestCase):

    def test_create_user_successfully(self):
        # @example.com is a reserved domain for testing purposes
        email = 'test@example.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        # We need to check the password using the check_password method, since the password is hashed
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email_cases = [
            ('test@EXAMPLE.COM', 'test@example.com'),
            ('Test@Example.COM', 'Test@example.com'),
            ('TEST@EXAMPLE.com', 'TEST@example.com'),
            ('TeSt@eXaMpLe.CoM', 'TeSt@example.com'),
        ]

        for input_email, expected_email in email_cases:
            """ subTest allows us to run the same test with different inputs. If one test fails, it will not stop the 
                others from running."""
            with self.subTest(input_email=input_email):
                user = get_user_model().objects.create_user(email=input_email, password='testpassword')
                self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        email_cases = [
            None,
            '',
        ]

        for email in email_cases:
            with self.subTest(email=email):
                with self.assertRaises(ValueError):
                    get_user_model().objects.create_user(email=email, password='testpassword')

    def test_create_superuser(self):
        email = 'superuser@example.com'
        password = 'superpassword'
        super_user = get_user_model().objects.create_superuser(email=email, password=password)
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            description='Sample recipe description',
            ingredients='Egg, Flour, Butter',
            preparation='Sample preparation description',
            time_minutes=5,
            price=Decimal('5.50')
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

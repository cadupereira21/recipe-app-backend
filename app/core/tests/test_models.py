"""We are going to use TestCase since it has built-in support for database transactions and rollbacks. Because of
that, it is considerably slower than SimpleTestCase, since it has a database setup overhead, but it is more suitable for testing models that interact with
the database."""
from django.test import TestCase
from django.contrib.auth import get_user_model


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
        # TODO: Parameterize this test to check different email formats

        email = 'test@EXAMPLE.com'

        user = get_user_model().objects.create_user(email=email, password='testpassword')

        self.assertEqual(user.email, email.lower())

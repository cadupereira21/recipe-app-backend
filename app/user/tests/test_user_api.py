from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class TestUserApiPublic(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {'email': 'test@example.com', 'password': 'testpass123', 'name': 'Test User'}
        response = self.client.post(CREATE_USER_URL, payload)
        created_user = get_user_model().objects.get(email=payload['email'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(created_user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_already_created(self):
        payload = {'email': 'test@example.com', 'password': 'testpass123', 'name': 'Test User'}
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {'email': 'test@example.com', 'password': 'pw', 'name': 'Test User'}
        response = self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)

    def test_create_token_success(self):
        user = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword123'
        }

        create_user(**user)

        response = self.client.post(CREATE_TOKEN_URL, {'email': user['email'], 'password': user['password']})

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        create_user(email='test@example.com', password='goodpass')

        payloads = [
            {'email': 'test@example.com', 'password': 'badpass'},
            {'email': 'test2@example.com', 'password': 'goodpass'},
            {'email': '', 'password': 'goodpass'},
            {'email': 'test@example.com', 'password': ''},
            {'email': '', 'password': ''}
        ]

        for payload in payloads:
            with self.subTest(payload=payload):
                response = self.client.post(CREATE_TOKEN_URL, payload)
                self.assertNotIn('token', response.data)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test api requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_authenticated(self):
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'email': self.user.email,
            'name': self.user.name,
        })

    def test_post_me_not_allowed(self):
        response = self.client.post(ME_URL, {})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {'name': 'Updated Name', 'password': 'newpassword123'}

        response = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

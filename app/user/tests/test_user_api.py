from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


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

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')


# We'll define the url as a function because we need to pass the recipe_id
def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    defaults = {
        'title': 'Sample title',
        'ingredients': 'Egg, Flour, Butter',
        'preparation': 'Sample preparation text',
        'time_minutes': 10,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf'
    }

    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(RECIPES_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testPass123'
        )
        self.client.force_authenticate(self.user)

    def test_list_recipes(self):
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        response = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'otherpass123',
        )

        create_recipe(user=other_user)
        create_recipe(user=self.user)

        response = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_recipe_details(self):
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)

        response = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create_recipe(self):
        payload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
        }

        response = self.client.post(RECIPES_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=response.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

        self.assertEqual(recipe.user, self.user)

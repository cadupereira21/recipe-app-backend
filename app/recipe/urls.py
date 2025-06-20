from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views

# Automatically create routes for the different objects of a view
router = DefaultRouter()
""" Create endpoint /recipe
    Since we are using ModelViewSet it is going to support all available HTTP methods
"""
router.register('recipe', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]

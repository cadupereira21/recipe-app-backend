from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    # Defines the object that will be managed by this view set
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """Override get_queryset to filter the get to retrieve only the recipes associated with the user from the request"""
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

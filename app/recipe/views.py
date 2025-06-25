from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeDetailSerializer
    # Defines the object that will be managed by this view set
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """Override get_queryset to filter the get to retrieve only the recipes associated with the user from the request"""
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    """This method is called by django when returning the details of a serializer
    This way, all endpoints will use the RecipeDetailSerializer, excepting the list action."""
    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        # This method is called after the validation
        # When creating a new recipe, set user with the request's authenticated user
        serializer.save(user=self.request.user)


class TagViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = serializers.TagSerializer
    # Defines the object that will be managed by this view set
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """Override get_queryset to filter the get to retrieve only the recipes associated with the user from the request"""
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

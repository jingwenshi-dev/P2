from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from recipes.serializers import *
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import status
from ..userdata.models import Rating, Comment, LikedRecipe, BrowsedRecipe
from itertools import chain



# Create your views here.
class PopularRecipes(ListAPIView):
    """
    Return a list of recipes based on its overall rating or the number of users marked them as favorite.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        recipes = Recipe.objects.annotate(num_likes=Count('liked')).order_by('-num_likes')
        return recipes


class MyRecipe(ListAPIView):
    """
    Return three list of recipes: Created, Liked, Interacted (create, like, rate, or comment)
    Note: You may want to use pagination.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer

    def list(self, request):
        user = request.user
        created = user.recipes.all()
        rated = user.rated.all().values_list('recipe')
        commented = user.commented.all().values_list('recipe')
        liked = user.liked.all().values_list('recipe')
        favorited = user.favorited.all().values_list('recipe')
        interacted = chain(created, rated, liked, commented)
        return JsonResponse({'created': created, 'favorited': favorited, 'interacted': interacted}, safe=False, status=status.HTTP_200_OK)


class SearchByName(ListAPIView):
    """
    Search recipes by name, ingredients, or creator.
    Then filter by cuisine, diet, or cooking time if these parameters are given.
    Finally, rank the recipes by their ratings and likes.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        # TODO
        pass


class SearchByIngredient(ListAPIView):
    """
    Search recipes by name, ingredients, or creator.
    Then filter by cuisine, diet, or cooking time if these parameters are given.
    Finally, rank the recipes by their ratings and likes.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        # TODO
        pass


class SearchByCreator(ListAPIView):
    """
    Search recipes by name, ingredients, or creator.
    Then filter by cuisine, diet, or cooking time if these parameters are given.
    Finally, rank the recipes by their ratings and likes.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        # TODO
        pass


class IngredientAutocomplete(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer

    def get_queryset(self):
        name = self.kwargs.get('name')
        return Ingredient.objects.filter(name__startswith=name)


class DisplayShoppingList():
    """
    Return combined ingredients and corresponding combined amount with unit.
    """
    # TODO
    pass

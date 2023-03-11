from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from accounts.models import User
from recipes.models import Recipe, Step, Ingredient, RecipeIngredient
from recipes.serializers import RecipeSerializer, StepSerializer, IngredientSerializer, RecipeIngredientSerializer


# Create your views here.
class CreateRecipeView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer


class CreateStepView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StepSerializer


#
# class GetCreateUpdateIngredientView(APIView):
#     """
#     Get the list of ingredient with all corresponding fields and ID.
#     If any ingredient DNE, create one it first.
#     """
#
#     def post(self, request, *args, **kwargs):
#
#         # Get current recipe
#         rid = self.kwargs.get("rid")
#         recipe = get_object_or_404(Recipe, rid)
#
#         # Get list of input ingredient in JSON
#         items = request.data.get('items', [])
#
#         lst = []
#
#         for item in items:
#
#             field_empty_err = []
#
#             name = item.get('name', '')
#             amount = item.get('amount', '')
#             unit = item.get('unit', '')
#
#             if name == '':
#                 errors = {"item": field_empty_err}
#
#         for item in items:
#             name = item.get('name', '')
#             amount = item.get('amount', '')
#             unit = item.get('unit', '')
#
#             # Get the ingredient, or create the ingredient if DNE
#             ingredient, created = Ingredient.objects.get_or_create(name=name)
#
#             # Link ingredient with recipe, or create that relation if DNE
#             recipe_ingredient, created = RecipeIngredient.objects.update_or_create(recipe=recipe, ingredient=ingredient,
#                                                                                    amount=amount, unit=unit)
#
#             lst.append({"id": pk, "name": name})
#
#         return JsonResponse({"items": lst})


class CreateIngredientView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer


class CreateRecipeIngredientView(CreateAPIView):
    """
    Create a unique combination of recipe and ingredient with a given amount and unit
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeIngredientSerializer


class GetUpdateDestroyRecipeIngredientView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeIngredientSerializer

    def get_object(self):
        """
        @return: A RecipeIngredient object based on the endpoint recipe and ingredient id.
        """
        rid = self.kwargs.get("rid", "")
        iid = self.kwargs.get("iid", "")

        recipe = get_object_or_404(Recipe, pk=rid)
        ingredient = get_object_or_404(Ingredient, pk=iid)

        recipe_ingredient = RecipeIngredient.objects.filter(recipe=recipe, ingredient=ingredient)

        if not recipe_ingredient.exists():
            raise NotFound(detail="The given combination of recipe and ingredient does not exist (Hint: Creat a new "
                                  "combination).")

        recipe_ingredient = recipe_ingredient[0]

        return recipe_ingredient


class GetUpdateDestroyStepView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StepSerializer

    def get_object(self):
        sid = self.kwargs.get("sid", "")
        step = get_object_or_404(Step, pk=sid)
        return step


class RecipeEditView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer

    def get_object(self):
        rid = self.kwargs.get("rid", "")
        recipe = get_object_or_404(Recipe, pk=rid)
        return recipe


class RecipeDetailView(APIView):
    def get(self, request, rid):
        recipe = get_object_or_404(Recipe, id=rid)
        step = Step.objects.filter(recipe=recipe)
        recipe_ingredient = RecipeIngredient.objects.filter(recipe=recipe)

        recipe_serializer = RecipeSerializer(recipe)
        step_serializer = StepSerializer(step, many=True)
        recipe_ingredient_serializer = RecipeIngredientSerializer(recipe_ingredient, many=True)

        return JsonResponse(
            {"recipe": recipe_serializer.data, "step": step_serializer.data, "recipe_ingredient": recipe_ingredient_serializer.data})

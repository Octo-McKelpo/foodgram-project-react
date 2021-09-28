from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .serializers import CreateRecipeSerializer
from .views import (IngredientViewSet, RecipeViewSet,
                    CustomUserViewSet, PurchaseListView, FavoriteViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/shopping_cart/',
         PurchaseListView.as_view(), name='add_recipe_to_shopping_cart'),
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteViewSet.as_view(), name='add_recipe_to_favorite'),
    path('recipes/<int:recipe_id>/edit', CreateRecipeSerializer.update,
         name='recipe_edit')
]

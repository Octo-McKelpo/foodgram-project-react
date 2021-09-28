from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                    CustomUserViewSet, PurchaseListView, FavoriteViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/shopping_cart/',
         PurchaseListView.as_view(), name='add_recipe_to_shopping_cart'),
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteViewSet.as_view(), name='add_recipe_to_favorite'),
    path('recipes/<int:recipe_id>/edit', RecipeViewSet.as_view(),
         name='recipe_edit')
]

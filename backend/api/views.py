from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (Favorite, Ingredient, PurchaseList, Recipe,
                            Follow, Tag, IngredientInRecipe, User)
from .filters import IngredientNameFilter, RecipeFilter
from .paginators import PageNumberPaginatorModified
from .permissions import AuthorOrReadOnly, IsOwnerOrAdminOrReadOnly
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, PurchaseListSerializer,
                          FollowSerializer, FollowerSerializer, TagSerializer,
                          RecipeListSerializer, UserSerializer)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPaginatorModified
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    serializer_class = UserSerializer

    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        data = {
            'user': user.id,
            'author': author.id,
        }
        serializer = FollowSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        subscribe = get_object_or_404(
            Follow, user=user, author=author
        )
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowerSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = CreateRecipeSerializer
    permission_classes = [AuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter
    pagination_class = PageNumberPaginatorModified

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeListSerializer
        return CreateRecipeSerializer

    @action(detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        data = {
            'user': user.id,
            'recipe': recipe.id,
        }
        serializer = PurchaseListSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorites = get_object_or_404(
            PurchaseList, user=user, recipe=recipe
        )
        favorites.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = user.purchases.all()
        list = {}
        for item in shopping_cart:
            recipe = item.recipe
            ingredients = IngredientInRecipe.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in list:
                    list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    list[name]['amount'] = (
                        list[name]['amount'] + amount
                    )

        shopping_list = []
        for item in list:
            shopping_list.append(f'{item} - {list[item]["amount"]} '
                                 f'{list[item]["measurement_unit"]} \n')
        response = HttpResponse(shopping_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'

        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None
    filter_backends = [IngredientNameFilter]
    search_fields = ['^name']


class FavoriteViewSet(APIView):
    def get(self, request, recipe_id):
        user = request.user.id
        data = {
            'user': user,
            'recipe': recipe_id
        }
        serializer = FavoriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        favorite_recipe = get_object_or_404(
            Favorite,
            user=user,
            recipe__id=recipe_id
        )
        favorite_recipe.delete()
        return Response(
            'Recipe is deleted from favorites',
            status.HTTP_204_NO_CONTENT
        )


class PurchaseListView(APIView):
    def get(self, request, recipe_id):
        user = request.user.id
        data = {
            'user': user,
            'recipe': recipe_id
        }
        serializer = PurchaseListSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        purchace_list_recipe = get_object_or_404(
            PurchaseList,
            user=user,
            recipe__id=recipe_id
        )
        purchace_list_recipe.delete()
        return Response(
            'Recipe is deleted from purchase list',
            status.HTTP_204_NO_CONTENT
        )

import django_filters as filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, User


class IngredientNameFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author']

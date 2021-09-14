import django_filters as filters
from recipe.models import Recipe, Tag
from rest_framework.filters import SearchFilter as BaseSearchFilter


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method='get_favorites')
    is_in_shopping_cart = filters.BooleanFilter(method='get_in_shopping_cart')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags',)

    def get_favorites(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(favorited_by__user=self.request.user)
        return Recipe.objects.all()

    def get_in_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(customers__user=self.request.user)
        return Recipe.objects.all()


class NameSearchFilter(BaseSearchFilter):
    search_param = 'name'

from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientInRecipe,
                            PurchaseList, Recipe, Follow, Tag)


class IngredientRecipeInLine(admin.TabularInline):
    model = IngredientInRecipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [IngredientRecipeInLine]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientRecipeInLine]


admin.site.register(Favorite)
admin.site.register(IngredientInRecipe)
admin.site.register(PurchaseList)
admin.site.register(Follow)
admin.site.register(Tag)

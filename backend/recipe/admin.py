from django.contrib import admin

from recipe.models import (
    Ingredient, IngredientInRecipe, Recipe, Tag,
    Favorite, PurchaseList, Subscribe
    )


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ("name",)


class TagAdmin(admin.ModelAdmin):
    pass


class AmountAdmin(admin.ModelAdmin):
    pass


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ("name",)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientInRecipe)
admin.site.register(Favorite)
admin.site.register(PurchaseList)
admin.site.register(Subscribe)

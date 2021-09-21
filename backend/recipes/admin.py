from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientInRecipe,
                            PurchaseList, Recipe, Subscribe, Tag)


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

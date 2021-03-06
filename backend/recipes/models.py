from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tag's name")
    color = models.CharField(max_length=100, blank=True,
                             verbose_name="Tag's color", default="")
    slug = models.SlugField(max_length=255, unique=True,
                            verbose_name="Tag's slug")

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f'Tag: {self.name}'


class Ingredient(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ingredient name",
                            unique=True)
    measurement_unit = models.CharField(max_length=30,
                                        verbose_name="Measurement unit")

    class Meta:
        ordering = ('name', )
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField(max_length=255, verbose_name="Recipe's title")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="recipes",
                               verbose_name="Recipe's author")
    tags = models.ManyToManyField(Tag, related_name="recipes",
                                  verbose_name="Recipe's tags")
    ingredients = models.ManyToManyField(
        Ingredient, through="IngredientInRecipe", related_name="recipes",
        verbose_name="Recipe's ingredients"
    )
    text = models.TextField(max_length=1000, verbose_name="Description")
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Cooking time", validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to="recipes/", blank=True,
                              verbose_name="Recipe's image", default="")
    pub_date = models.DateTimeField(
        verbose_name="Publication date",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f'Recipe: {self.name} by {self.author.first_name}'


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ingredient',
        on_delete=models.CASCADE,
        related_name='ingredients_amounts',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipe',
        on_delete=models.CASCADE,
        related_name='ingredients_amounts',
    )
    amount = models.PositiveIntegerField(verbose_name='Amount')

    class Meta:
        verbose_name = 'Ingredient in a recipe'
        verbose_name_plural = 'Ingredients in a recipe'
        unique_together = ('ingredient', 'recipe')

    def __str__(self):
        return (f'{self.ingredient.name} - {self.amount}'
                f' {self.ingredient.measurement_unit}')


class PurchaseList(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Purchase',
        on_delete=models.CASCADE,
        related_name='customers'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date when added'
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='purchase_user_recipe_unique'
            )
        ]

    def __str__(self):
        return f'Purchase: {self.recipe.name}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user} is subscribed for {self.author}'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipe',
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    user = models.ForeignKey(
        User,
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='favored_recipes'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe'
            )
        ]
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'

    def __str__(self):
        return f'{self.user}. Recipe: {self.recipe.id}.{self.recipe.name}'

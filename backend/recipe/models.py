from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ingredient name",
                            unique=True)
    measure = models.CharField(max_length=30, verbose_name="Measure")

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return f'Ingredient: {self.name} ({self.measure})'


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tag's name")
    color = models.CharField(max_length=100, blank=True,
                             verbose_name="Tag's color", default="")
    slug = AutoSlugField(max_length=255, allow_unicode=True, unique=True,
                         verbose_name="Tag's slug")

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f'Tag: {self.name}'


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
    description = models.TextField(max_length=1000, verbose_name="Description")
    cook_time = models.PositiveSmallIntegerField(verbose_name="Cooking time",
                                                 validators=[
                                                     MinValueValidator(1)])
    image = models.ImageField(upload_to="recipes/", blank=True,
                              verbose_name="Recipe's image", default="")
    slug = AutoSlugField(populate_from="name", allow_unicode=True, unique=True,
                         editable=True, verbose_name="Slug")
    favorite = models.ManyToManyField(User, blank=True,
                                      related_name="favorite_recipes",
                                      verbose_name="Added to favorites",
                                      default="")
    listed = models.ManyToManyField(User, blank=True,
                                    related_name="listed_recipes",
                                    verbose_name="Added to cart",
                                    default="")
    pub_date = models.DateTimeField(
        verbose_name="Publication date",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f'Recipe: {self.name} by {self.author.first_name}'


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipe',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ingredient',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField('Amount')

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
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

    def __str__(self):
        return f'Purchase: {self.recipe.name}'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        on_delete=models.CASCADE
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

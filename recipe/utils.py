import io
import math
import os
from decimal import Decimal

from django.core.exceptions import MultipleObjectsReturned
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from foodgram.settings import ALLOWED_TAGS
from recipe.models import Amount, Ingredient, Recipe


def save_form_m2m(request, form):
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            ingredients = get_ingredients_from(request.POST)
            amounts = check_and_convert_to_objects(ingredients, recipe)
            Amount.objects.bulk_create(amounts)
            form.save_m2m()
            return recipe
    except IntegrityError:
        return HttpResponseBadRequest


def get_ingredients_from(post):
    ingredients = {}
    for key, name in post.items():
        if key.startswith("nameIngredient"):
            value = key.replace("name", "value")
            ingredients[name] = post[value]
    return ingredients


def check_and_convert_to_objects(ingredients, recipe):
    amounts = []
    for name, amount in ingredients.items():
        amount = math.fabs(Decimal(amount.replace(",", ".")))
        try:
            ingredient = get_object_or_404(Ingredient, name__exact=name)
            amounts.append(
                Amount(recipe=recipe, ingredient=ingredient, amount=amount))
        except MultipleObjectsReturned:
            pass
    return amounts


def combine_ingredients(request):
    if request.user.is_authenticated:
        recipes = request.user.listed_recipes.all()
    else:
        recipes = get_session_recipes(request)
    amounts = Amount.objects.filter(recipe__in=recipes)
    combined_ingredients = {}
    for amount in amounts:
        amount_name = f"{amount.ingredient.name}, {amount.ingredient.measure}"
        combined_ingredients[amount_name] = combined_ingredients.get(
            amount_name, 0) + amount.amount

    return combined_ingredients


def generate_pdf(combined_ingredients):
    buffer = io.BytesIO()
    ingredients_to_buy = canvas.Canvas(buffer)
    text_object = ingredients_to_buy.beginText()
    text_object.setTextOrigin(inch, 11 * inch)
    text_object.setFont("Helvetica", 14)
    for key, value in combined_ingredients.items():
        text_object.textLine(f"{key}: {value}")
    ingredients_to_buy.drawText(text_object)
    ingredients_to_buy.showPage()
    ingredients_to_buy.save()
    buffer.seek(0)
    return buffer


def get_tags_from(request):
    tags = set()
    if "tags" in request.GET:
        tags = set(request.GET.getlist("tags"))
        tags.intersection_update(set(ALLOWED_TAGS))
    return tags


def get_session_recipes(request):
    if request.session.get("cart") is not None:
        cart = request.session.get("cart")
        return Recipe.objects.filter(id__in=cart)


def filter_by_tags(recipes, tags):
    return recipes.filter(tags__name__in=tags).distinct()

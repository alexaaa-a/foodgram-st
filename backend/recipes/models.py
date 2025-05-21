from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    measurement_unit = models.CharField(
        max_length=100,
        verbose_name="Единица измерения",
    )

    class Meta:
        verbose_name = "ингредиент"
        verbose_name_plural = "Ингредиенты"


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    name = models.CharField(
        max_length=256,
        verbose_name="Название",
    )
    image = models.ImageField(
        upload_to="recipes/",
        verbose_name="Картинка",
    )
    text = models.TextField(
        verbose_name="Описание",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        verbose_name="Ингредиенты",
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Время приготовления",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время публикации",
    )

    class Meta:
        verbose_name = "рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-created_at"]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
    )
    amount = models.IntegerField()

    class Meta:
        verbose_name = "рецепт и ингредиент"
        verbose_name_plural = "Рецепты и ингредиенты"

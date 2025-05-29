import base64
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer
from users.models import User, Favourite
from rest_framework import serializers
from recipes.models import Ingredient, Recipe, RecipeIngredient


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredient.id")
    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image/"):
            format, image = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(image), name="temp." + ext)
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "avatar",
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id",
                  "email",
                  "username",
                  "first_name",
                  "last_name",
                  "password"
                  )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True, allow_null=False)
    ingredients = RecipeIngredientWriteSerializer(many=True, write_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        ]
        read_only_fields = ("author",)

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.in_favourites.filter(user=request.user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.in_shopping_carts.filter(user=request.user).exists()
        return False

    def validate(self, data):
        if "ingredients" not in self.initial_data:
            raise serializers.ValidationError(
                {"ingredients": "Обязательное поле"}
            )
        elif not self.initial_data["ingredients"]:
            raise serializers.ValidationError(
                {"ingredients": "Не должно быть пустым"}
            )
        return data

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients", [])

        ingredient_ids = [ing["id"] for ing in ingredients_data]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                {"ingredients": "Обнаружены дубликаты ингредиентов"},
                code="duplicate_ingredients",
            )

        recipe = Recipe.objects.create(
            author=self.context["request"].user, **validated_data
        )
        self._save_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients", [])

        ingredient_ids = [ing["id"] for ing in ingredients_data]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                {"ingredients": "Обнаружены дубликаты ингредиентов"},
                code="duplicate_ingredients",
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        self._save_ingredients(instance, ingredients_data)
        return instance

    def _save_ingredients(self, recipe, ingredients_data):
        RecipeIngredient.objects.filter(recipe=recipe).delete()

        recipe_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient["id"],
                amount=ingredient["amount"]
            )
            for ingredient in ingredients_data
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def get_ingredients(self, obj):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientReadSerializer(
            recipe_ingredients,
            many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["is_favorited"] = self.get_is_favorited(instance)
        representation["is_in_shopping_cart"] = self.get_is_in_shopping_cart(
            instance
        )

        representation["ingredients"] = RecipeIngredientReadSerializer(
            RecipeIngredient.objects.filter(recipe=instance), many=True
        ).data
        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    image = Base64ImageField(read_only=True)
    cooking_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Favourite
        fields = ("id", "name", "image", "cooking_time")


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
            "avatar",
        )

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        lst = getattr(obj, "limited_recipes", None)
        if lst is not None:
            return len(lst)
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes = getattr(obj, "limited_recipes", None)
        if recipes is None:
            recipes = obj.recipes.all().order_by("-created_at")
        return ShortRecipeSerializer(recipes, many=True).data

    def validate_following(self, value):
        if self.context["request"].user == value:
            return serializers.ValidationError("You cannot follow yourself")
        return value


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")

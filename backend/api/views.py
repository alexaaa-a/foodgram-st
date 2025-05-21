from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    UserSerializer,
    FavoriteSerializer,
    SubscriptionSerializer,
    ShoppingCartSerializer,
)
from recipes.models import Ingredient, Recipe
from djoser.views import UserViewSet
from users.models import User, Follow, ShoppingCart
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    CharFilter,
    BooleanFilter,
)
from .permissions import IsAuthorOrReadOnly
from users.models import Favourite
from rest_framework import filters


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = BooleanFilter(method="filter_is_in_shopping_cart")

    class Meta:
        model = Recipe
        fields = ["author"]

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none() if value else queryset
        return (
            queryset.filter(in_favourites__user=user)
            if value
            else queryset.exclude(in_favourites__user=user)
        )

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none() if value else queryset
        return (
            queryset.filter(in_shopping_carts__user=user)
            if value
            else queryset.exclude(in_shopping_carts__user=user)
        )


class CustomFilter(FilterSet):
    name = CharFilter(
        field_name="name",
        lookup_expr="istartswith",
    )

    class Meta:
        model = Ingredient
        fields = ["name"]


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "limit"
    page_query_param = "page"
    max_page_size = 100


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomFilter
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class PublicUserViewSet(UserViewSet):
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        users = User.objects.all()
        return users

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(
        detail=False,
        methods=["put", "delete"],
        url_path="me/avatar",
        permission_classes=[permissions.IsAuthenticated],
    )
    def set_avatar(self, request):
        if request.method == "PUT":
            if not request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSerializer(
                self.request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {"avatar": serializer.data["avatar"]},
                status=status.HTTP_200_OK
            )

        else:
            if request.user.avatar:
                request.user.avatar.delete()
                request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        recipes_limit = request.query_params.get("recipes_limit")
        try:
            recipes_limit = int(recipes_limit) if recipes_limit else None
        except ValueError:
            recipes_limit = None

        user = request.user
        following_users = user.follower.all().values_list(
            "following",
            flat=True
        )
        queryset = (
            User.objects.filter(id__in=following_users).prefetch_related(
                "recipes"
            ))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionSerializer(
                page,
                many=True,
                context={"request": request, "recipes_limit": recipes_limit},
            )
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionSerializer(
            queryset,
            many=True,
            context={"request": request, "recipes_limit": recipes_limit},
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = get_object_or_404(User, id=id)

        if request.method == "POST":
            recipes_limit = request.query_params.get("recipes_limit")
            try:
                recipes_limit = int(recipes_limit) if recipes_limit else None
            except ValueError:
                recipes_limit = None

            exists = Follow.objects.filter(
                user=request.user,
                following=user,
            ).exists()

            if request.user == user or exists:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            Follow.objects.create(
                user=request.user,
                following=user,
            )

            serializer = SubscriptionSerializer(
                user,
                many=False,
                context={
                    "request": request,
                    "recipes_limit": recipes_limit,
                },
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            try:
                subscription = Follow.objects.get(
                    user=request.user,
                    following=user,
                )

            except Follow.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            subscription.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    pagination_class = CustomPageNumberPagination
    filterset_class = RecipeFilter
    ordering_fields = ("-created_at",)

    @action(
        detail=True,
        methods=["GET"],
        url_name="get_link",
        url_path="get-link",
    )
    def get_link(self, request, pk):
        get_object_or_404(Recipe, id=pk)
        link = request.build_absolute_uri(f"/recipes/{pk}/")
        return Response({"short-link": link}, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == "POST":
            favorite, created = Favourite.objects.get_or_create(
                user=request.user, recipe=recipe
            )

            if not created:
                return Response(
                    {"error": "Рецепт уже в избранном"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = FavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            deleted_count, _ = Favourite.objects.filter(
                user=request.user, recipe=recipe
            ).delete()

            if deleted_count == 0:
                return Response(
                    {"error": "Рецепт не найден в избранном"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        if request.method == "POST":
            cart_item, created = ShoppingCart.objects.get_or_create(
                user=user,
                recipe=recipe,
            )

            if not created:
                return Response(
                    {"error": "Рецепт уже в корзине"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = ShoppingCartSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            deleted_count, _ = ShoppingCart.objects.filter(
                user=user, recipe=recipe
            ).delete()

            if deleted_count == 0:
                return Response(
                    {"error": "Рецепт не найден в корзине"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[
            permissions.IsAuthenticated,
        ],
    )
    def download_shopping_cart(self, request):
        recipes = Recipe.objects.filter(
            in_shopping_carts__user=request.user,
        )

        serializer = RecipeSerializer(recipes, many=True)
        data = serializer.data

        result = {}

        for recipe in data:
            for ingredient_data in recipe["ingredients"]:
                name = ingredient_data["name"]
                amount = ingredient_data["amount"]
                unit = ingredient_data["measurement_unit"]

                if name not in result:
                    result[name] = [amount, unit]
                else:
                    result[name][0] += amount

        file_content = "Список покупок:\n\n"
        for key, value in result.items():
            file_content += f"{key} - {value[0]} {value[1]}\n"

        response = HttpResponse(
            content=file_content, content_type="text/plain; charset=utf-8"
        )
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.txt"')
        return response

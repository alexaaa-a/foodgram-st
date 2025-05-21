from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, PublicUserViewSet, RecipeViewSet

router = routers.DefaultRouter()

router.register(
    "ingredients",
    IngredientViewSet,
    basename="ingredient",
)
router.register(
    r"users",
    PublicUserViewSet,
    basename="user",
)
router.register(
    r"recipes",
    RecipeViewSet,
    basename="recipe",
)

urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
    path("", include("djoser.urls")),
]

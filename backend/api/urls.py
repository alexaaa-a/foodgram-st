from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, PublicUserViewSet, RecipeViewSet

router = routers.DefaultRouter()

router.register(
    "ingredients",
    IngredientViewSet,
    basename="ingredients",
)
router.register(
    r"users",
    PublicUserViewSet,
    basename="users",
)
router.register(
    r"recipes",
    RecipeViewSet,
    basename="recipes",
)

urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
    path("", include("djoser.urls")),
]

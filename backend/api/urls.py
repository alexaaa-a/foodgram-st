from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers
from . import reset_password_views
from .views import IngredientViewSet, PublicUserViewSet, RecipeViewSet
from ws.views import websocket_interface


app_name = "api"

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
    path('accounts/', include('allauth.urls')),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path(
        "github-login/",
        TemplateView.as_view(template_name="oauth_forms/github_login.html"),
        name="github_login_page"
    ),
]

urlpatterns += [
    path(
        "reset-password/",
        reset_password_views.reset_password_request,
        name="reset_password"
    ),
    path(
        "reset-password-confirm/<uidb64>/<token>/",
        reset_password_views.reset_password_confirm,
        name="reset_password_confirm"
    ),
]

urlpatterns += [
    path('ws-interface/', websocket_interface),
]

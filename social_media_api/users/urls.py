from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("sign_up", views.RegisterViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("change_password/", views.change_password, name="change_password"),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]

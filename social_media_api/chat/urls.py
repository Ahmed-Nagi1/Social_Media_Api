from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("manage-group", views.ManageGroup, basename="create-group")

urlpatterns = [
    path("", include(router.urls)),
    path("groups/<pk>/join/", views.ManageGroup.as_view({"post": "join_group"})),
    path("chat-group/<str:room_name>/", views.chat_room, name="chat_room"),
]

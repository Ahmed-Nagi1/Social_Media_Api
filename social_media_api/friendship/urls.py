from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(
    "send-request-friend", views.FriendRequestViewSet, basename="send_friend_request"
)
router.register(
    "list-request-friend", views.ListRequestFriends, basename="list_request_friends"
)
router.register("list-my-friends", views.ListMyFriends, basename="list_my_friends")
router.register("delete-my-friends", views.DeleteMyFriend, basename="delete_my_friends")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "delete-request/",
        views.FriendRequestViewSet.as_view({"post": "delete-request"}),
    ),
    path("approval-of-requests/", views.approval_of_requests),
]

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("author", views.PostAuthorView, basename="author_post")
router.register("viewers", views.PostViewersView, basename="viewers_post")
router.register("comment", views.CommentViewSet, basename="comment_post")
router.register("react", views.ReactionViewSet, basename="react_post")

urlpatterns = [path("", include(router.urls))]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("author", views.PostAuthorView, basename="author_post")
router.register("viewers", views.PostViewersView, basename="viewers_post")
router.register("comment", views.CommentViewSet, basename="comment_post")
router.register("react", views.ReactionViewSet, basename="react_post")

urlpatterns = router.urls

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('manage-group', views.ManageGroup, basename='create-group')

urlpatterns = [
    path("", include(router.urls)),

]

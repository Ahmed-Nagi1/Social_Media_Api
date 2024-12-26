from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comment, Posts, Reaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class PostsAuthorSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posts
        fields = ["url", "content", "image", "created_at", "updated_at"]
        read_only_fields = ["url", "created_at", "updated_at"]
        extra_kwargs = {
            "image": {"required": False},
            'url': {'view_name': 'author_post-detail'}  # This is the name of the view
        }
        


class PostsViewersSerializers(serializers.HyperlinkedModelSerializer):
    author = UserSerializer()
    class Meta:
        fields = ["url", "author", "content", "image", "created_at", "updated_at"]
        model = Posts
        extra_kwargs = {
            'url': {'view_name': 'viewers_post-detail'}  # This is the name of the view
        }


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["author"]


class ReactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        exclude = ["author"]

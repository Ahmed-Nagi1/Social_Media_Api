from rest_framework import serializers

from .models import Comment, Posts, Reaction


class PostsAuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ["pk", "content", "image", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {"image": {"required": False}}


class PostsViewersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Posts
        exclude = ["id"]


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["author"]


class ReactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        exclude = ["author"]

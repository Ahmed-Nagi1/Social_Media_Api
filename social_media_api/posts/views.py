from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Comment, Posts, Reaction
from .serializers import (
    CommentSerializers,
    PostsAuthorSerializers,
    PostsViewersSerializers,
    ReactionSerializers,
)


class PostAuthorView(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = PostsAuthorSerializers

    def get_queryset(self):
        return Posts.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)


class PostViewersView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsViewersSerializers
    queryset = Posts.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get("post")
        post = Posts.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializers
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        post_id = self.request.data.get("post")
        post = Posts.objects.get(id=post_id)
        existing_reaction = Reaction.objects.filter(
            post=post,
            author=self.request.user,
        ).first()

        print(self.request.data) 
        reaction_type = self.request.data.get("reaction_type")
        if reaction_type not in ["like", "unlike"]:
            raise ValidationError({"reaction_type": "Invalid reaction type."})

        if existing_reaction:
            if reaction_type == "unlike":
                existing_reaction.delete()
                post.reactions_count -= 1
            else:
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
        elif reaction_type != "unlike":
            post.reactions_count += 1
            serializer.save(author=self.request.user, post=post)
        post.save()

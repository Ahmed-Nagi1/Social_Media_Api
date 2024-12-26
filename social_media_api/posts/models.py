from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
import uuid

class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, verbose_name=_("author"), on_delete=models.CASCADE)
    content = models.TextField(_("content"))
    image = models.ImageField(
        _("image"),
        upload_to="posts/image/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)


class Comment(models.Model):
    post = models.ForeignKey(
        Posts,
        related_name="comments",
        verbose_name=_("post"),
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(User, verbose_name=_("author"), on_delete=models.CASCADE)
    content = models.TextField(_("content"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


class Reaction(models.Model):

    REACTION_CHOICES = [
        ("like", "Like"),
        ("unlike", "Unlike"),
    ]

    post = models.ForeignKey(
        Posts,
        related_name="reactions",
        verbose_name=_("post"),
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(User, verbose_name=_("author"), on_delete=models.CASCADE)
    reaction_type = models.CharField(
        _("reaction type"),
        max_length=10,
        choices=REACTION_CHOICES,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        unique_together = ("post", "author")

    def __str__(self):
        return f"Reaction by {self.author} on {self.post}"

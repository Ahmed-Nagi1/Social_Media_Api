from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

class Posts(models.Model):
    author = models.ForeignKey(User, verbose_name=_("author"), on_delete=models.CASCADE)
    content = models.TextField(_("content"))
    reactions_count = models.IntegerField(_("reactions count"), default=0)
    image = models.ImageField(_("image"), upload_to='posts/image/', blank=True, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)


class Comment(models.Model):
    post = models.ForeignKey(Posts, related_name="comments", verbose_name=_("post"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("author"), on_delete=models.CASCADE)
    content = models.TextField(_("content"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
    

class Reaction(models.Model):

    REACTION_CHOICES = [
        ('like', 'Like'),
        ('unlike', 'Unlike'),
    ]

    post = models.ForeignKey(Posts, related_name="reactions", verbose_name=_("post"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("author"), on_delete=models.CASCADE)
    reaction_type = models.CharField(_("reaction type"), max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        unique_together = ('post', 'author')

    def __str__(self):
        return f'Reaction by {self.author} on {self.post}'

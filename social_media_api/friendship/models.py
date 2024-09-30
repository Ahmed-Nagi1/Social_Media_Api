from django.contrib.auth.models import User
from django.db import models


class Friendship(models.Model):
    REQUESTED = "requested"
    ACCEPTED = "accepted"

    STATUS_CHOICES = [
        (REQUESTED, "Requested"),
        (ACCEPTED, "Accepted"),
    ]

    from_user = models.ForeignKey(
        User,
        related_name="sent_requests",
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        User,
        related_name="received_requests",
        on_delete=models.CASCADE,
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} : {self.status}"


class MyFriends(models.Model):
    me = models.ForeignKey(User, on_delete=models.CASCADE)
    myFriend = models.ForeignKey(
        User,
        related_name="my_friends",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.me}"

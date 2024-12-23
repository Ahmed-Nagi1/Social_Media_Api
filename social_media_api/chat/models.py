import uuid
from django.contrib.auth.models import User
from django.db import models


def generate_uuid():
    return str(uuid.uuid4())[:13]


class GroupsManage(models.Model):
    groupID = models.CharField(
        primary_key=True,
        default=generate_uuid,
        editable=False,
        unique=True,
        max_length=255
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class GroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupsManage, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "group")


class MessageGroup(models.Model):
    group = models.ForeignKey(GroupsManage, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} in {self.group.name}: {self.content[:20]}"

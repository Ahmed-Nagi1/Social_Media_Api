from django.db import models
import uuid
from django.contrib.auth.models import User



class GroupsManage(models.Model):
    def generate_uuid():
        return str(uuid.uuid4())[:13]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    groupID = models.CharField(primary_key=True, default=generate_uuid, editable=False, unique=True)

    def __str__(self) -> str:
        return f"{self.name}_{str(self.groupID)[:13]}"
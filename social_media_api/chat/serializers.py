from rest_framework import serializers

from .models import GroupsManage


class ManageGroupSerializer(serializers.Serializer):
    group_name = serializers.CharField(required=False)
    delete_id = serializers.CharField(required=False)


class ManageGroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupsManage
        fields = ["name", "groupID"]

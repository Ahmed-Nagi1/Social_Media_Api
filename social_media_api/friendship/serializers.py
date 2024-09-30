from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Friendship, MyFriends


class SendFriendRequestSerializers(serializers.Serializer):
    to_user = serializers.IntegerField()

    class Meta:
        model = Friendship
        fields = ["from_user", "to_user", "status"]

    extra_kwargs = {
        "to_user": {"required": True},
    }

    def validate_to_user(self, value):
        try:
            user = User.objects.get(id=value)

        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return user


class ListFriendRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ["to_user", "status"]


class ListFriendsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ["from_user", "created_at"]


class ApprovalOfRequestsSerializers(serializers.Serializer):
    add_userID = serializers.IntegerField()

    class Meta:
        model = MyFriends
        fields = ["myFriend"]

    def validate_add_userID(self, value):
        try:
            user_add = User.objects.get(id=value)

        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return user_add


class ListMyFriendsSerializers(serializers.ModelSerializer):
    class Meta:
        model = MyFriends
        fields = ["myFriend"]


class DeleteMyFriendSerializers(serializers.Serializer):
    userID = serializers.IntegerField()

    class Meta:
        model = MyFriends
        fields = ["myFriend"]

    def validate_userID(self, value):
        try:
            user = User.objects.get(id=value)

        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return user

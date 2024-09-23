from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes

from .models import Friendship, MyFriends
from .serializers import (
    SendFriendRequestSerializers,
    ListFriendRequestSerializers,
    ListFriendsSerializers,
    ApprovalOfRequestsSerializers,
    ListMyFriendsSerializers,
    DeleteMyFriendSerializers,
)


class FriendRequestViewSet(viewsets.ModelViewSet):
    # This viewset manages sending, listing, and deleting friend requests
    # It ensures a user cannot send a friend request to themselves or duplicate requests

    serializer_class = SendFriendRequestSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(from_user=self.request.user.id)

    def get_serializer_class(self):
        if self.action == "list":
            return ListFriendRequestSerializers
        return SendFriendRequestSerializers

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ListFriendRequestSerializers(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Check if the sender and receiver are the same person
        # Also, prevent sending duplicate friend requests

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_user = request.user
        to_user = serializer.validated_data["to_user"]

        if from_user.id == to_user.id:
            return Response(
                {"error": "cannot send to your self!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Friendship.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response(
                {"error": "Friend request already sent."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Friendship.objects.create(
            from_user=from_user, to_user=to_user, status=Friendship.REQUESTED
        )

        return Response(
            {"message": "Friend request sent successfully."},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"], url_path="delete-request")
    def delete_request(self, request, *args, **kwargs):
        # Delete sent request

        from_user = request.user
        user_delete = request.data.get("user_delete")

        if not user_delete:
            return Response(
                {"error": "user_delete is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friendship = Friendship.objects.filter(from_user=from_user, to_user=user_delete)

        if friendship.exists():
            friendship.delete()
            return Response({"status": "OK"}, status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND
        )


class ListRequestFriends(viewsets.ModelViewSet):
    # This viewset retrieves and lists all friend requests sent to the logged-in user

    serializer_class = ListFriendsSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(to_user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approval_of_requests(requests):
    # This function handles the approval of received friend requests
    # It creates a friendship if the request is valid and not already approved

    serializer = ApprovalOfRequestsSerializers(data=requests.data)
    if serializer.is_valid():
        user_add = serializer.validated_data.get("add_userID")
        user = requests.user
        check_user = Friendship.objects.filter(
            from_user=user_add, to_user=user
        ).exists()
        check_friend = MyFriends.objects.filter(me=user, myFriend=user_add).exists()
        if check_user:
            if check_friend:
                return Response(
                    {"error": "is already friends"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                MyFriends.objects.create(me=user, myFriend=user_add)

                return Response({"success": "Friendship created successfully"})

        return Response(
            {"error": "user not found!"}, status=status.HTTP_400_BAD_REQUEST
        )



class ListMyFriends(viewsets.ModelViewSet):
    # This viewset lists all friends of the currently logged-in user

    serializer_class = ListMyFriendsSerializers
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get_queryset(self):
        return MyFriends.objects.filter(me=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DeleteMyFriend(viewsets.ModelViewSet):
    # This viewset allows a user to remove a friend from their friend list

    serializer_class = DeleteMyFriendSerializers
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        # Try to find the friend relationship, and if found, delete it
        # Return an error if the user is not a friend

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            friend = serializer.validated_data["userID"]

            try:
                friend_relationship = MyFriends.objects.get(me=user, myFriend=friend)
            except MyFriends.DoesNotExist:
                return Response(
                    {"detail": "This user is not your friend."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            friend_relationship.delete()
            return Response(
                {"detail": "Friendship deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

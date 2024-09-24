from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from .models import GroupsManage
from .serializers import (
    ManageGroupSerializer,
    ManageGroupListSerializer,
)



class ManageGroup(viewsets.ModelViewSet):
    serializer_class = ManageGroupSerializer
    permission_classes = [IsAuthenticated]
    queryset = GroupsManage.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = GroupsManage.objects.filter(owner=self.request.user)
        serializer = ManageGroupListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if GroupsManage.objects.filter(owner=request.user).count() >=10:
            return Response({"error":"reached the limit"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data.get('group_name')
            GroupsManage.objects.create(owner=request.user, name=name)
            return Response({"status": "OK"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            group_id = serializer.validated_data["delete_id"]
            group = GroupsManage.objects.filter(owner=user, groupID=group_id)
            if group:
                group.delete()
                return Response(
                    {"detail": "Group deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            return Response({"error":"Not found group"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
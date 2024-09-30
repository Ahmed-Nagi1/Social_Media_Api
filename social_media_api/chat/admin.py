from django.contrib import admin

from .models import GroupsManage, GroupMembership


class GroupsManageAdmin(admin.ModelAdmin):
    list_display = ("groupID", "name", "owner")
    search_fields = ("name", "owner__username")
    list_filter = ("owner",)

admin.site.register(GroupsManage, GroupsManageAdmin)


class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "group")
    search_fields = ("name", "user__username")


admin.site.register(GroupMembership, GroupMembershipAdmin)

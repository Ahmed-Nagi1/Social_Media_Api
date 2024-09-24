from django.contrib import admin

from .models import GroupsManage


class GroupsManageAdmin(admin.ModelAdmin):
    list_display = ('groupID', 'name', 'owner')
    search_fields = ('name', 'owner__username')
    list_filter = ('owner',)


admin.site.register(GroupsManage, GroupsManageAdmin)
from django.contrib import admin

from .models import Friendship, MyFriends

admin.site.register(Friendship)
admin.site.register(MyFriends)

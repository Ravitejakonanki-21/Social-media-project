from django.contrib import admin
from .models import FriendRequest, Follow


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "accepted", "created_at"]
    list_filter = ["accepted", "created_at"]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["follower", "following", "id"]

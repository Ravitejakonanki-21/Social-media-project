from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendRequest, Follow
from notifications.models import Notification


@receiver(post_save, sender=FriendRequest)
def notify_friend_request(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=f"{instance.sender.username} sent you a friend request.",
        )


@receiver(post_save, sender=Follow)
def notify_follow(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.following,
            message=f"{instance.follower.username} started following you.",
        )

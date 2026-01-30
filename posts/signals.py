from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post, Comment
from notifications.models import Notification


@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created and instance.author != instance.post.author:
        Notification.objects.create(
            user=instance.post.author,
            message=f"{instance.author.username} commented on your post.",
        )


def notify_like(sender, instance, action, pk_set, **kwargs):
    if action != "post_add":
        return
    for user_pk in pk_set:
        from django.contrib.auth.models import User
        liker = User.objects.get(pk=user_pk)
        if liker != instance.author:
            Notification.objects.create(
                user=instance.author,
                message=f"{liker.username} liked your post.",
            )


m2m_changed.connect(notify_like, sender=Post.likes.through)
